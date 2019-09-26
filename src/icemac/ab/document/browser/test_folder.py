# -*- coding: utf-8 -*-
import icemac.addressbook.testing
import pytest
import transaction
import zope.testbrowser.browser


# Fixtures to set-up infrastructure which are usable in tests:


@pytest.yield_fixture(scope='function')
def folders_and_users(folders_and_usersS):
    """Provide predefined folders, see `folders_and_usersS`."""
    for connection in icemac.addressbook.testing.pyTestStackDemoStorage(
            folders_and_usersS.zodb, 'folders'):
        for address_book in icemac.addressbook.testing.site(connection):
            yield address_book


# Infrastructure fixtures

@pytest.yield_fixture(scope='session')
def folders_and_usersS(
        addressBookS, KeywordFactory, UserFactory, FolderFactory):
    r"""Create base data used in folder tests:

    Folders: (r/o and r/w show the name of the keywords needed to access the
              folder)

    +----------------+
    | name: Top 1    |
    | r/o:  ro1, or1 |
    | r/w:  rw1      |
    +----------------+
           ||
           \/
    +-------------+
    | name: Sub 2 |
    | r/o:  ro2   |
    | r/w:        |
    +-------------+
           ||
           \/
    +----------------+
    | name: Sub 3    |
    | r/o:  or3      |
    | r/w:  rw3, wr3 |
    +----------------+

    Users: (name + "@example.com" is the login-name; after the colon the
            groups aka keywords of the user are listed, the password is
            "password")

    u_or1: or1
    u_ro1_rw1: ro1, rw1
    u_or3: or3
    u_rw3: rw3

    """
    for connection in icemac.addressbook.conftest.pyTestStackDemoStorage(
            addressBookS, 'FoldersAndUsersSession'):
        for address_book in icemac.addressbook.conftest.site(connection):
            ro1 = KeywordFactory(address_book, u'ro1')
            or1 = KeywordFactory(address_book, u'or1')
            rw1 = KeywordFactory(address_book, u'rw1')
            ro2 = KeywordFactory(address_book, u'ro2')
            or3 = KeywordFactory(address_book, u'or3')
            rw3 = KeywordFactory(address_book, u'rw3')
            wr3 = KeywordFactory(address_book, u'wr3')

            top1 = FolderFactory(address_book, u'Top 1',
                                 read_only=[ro1, or1], read_write=[rw1])
            sub2 = FolderFactory(address_book, u'Sub 2', parent=top1,
                                 read_only=[ro2])
            FolderFactory(address_book, u'Sub 3', parent=sub2,
                          read_only=[or3], read_write=[rw3, wr3])

            UserFactory(address_book, u'u_or1', u'u_or1', u'u_or1@example.com',
                        u'password', roles=[u'Document user'],
                        keywords=[or1])
            UserFactory(address_book, u'u_ro1_rw1', u'u_ro1_rw1',
                        u'u_ro1_rw1@example.com', u'password',
                        roles=[u'Document user'], keywords=[ro1, rw1])
            UserFactory(address_book, u'u_or3', u'u_or3', u'u_or3@example.com',
                        u'password', roles=[u'Document user'],
                        keywords=[or3])
            UserFactory(address_book, u'u_rw3', u'u_rw3', u'u_rw3@example.com',
                        u'password', roles=[u'Document user'],
                        keywords=[rw3])
        transaction.commit()
        yield connection


def test_folder__Add__List__Edit__Delete__1(
        address_book, KeywordFactory, browser):
    """They allow to CRUD a new folder."""
    KeywordFactory(address_book, u'kw1')
    KeywordFactory(address_book, u'kw2')
    KeywordFactory(address_book, u'kw3')
    browser.login('mgr')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)

    # Add
    browser.getLink('folder').click()
    assert browser.FOLDER_ADD_URL == browser.url
    browser.getControl('folder title').value = 'föø'
    assert (['kw1', 'kw2', 'kw3'] ==
            browser.getControl('read only access').displayOptions)
    browser.getControl('read only access').displayValue = ['kw1', 'kw3']
    assert (['kw1', 'kw2', 'kw3'] ==
            browser.getControl('read and write access').displayOptions)
    browser.getControl('read and write access').displayValue = ['kw2']
    browser.getControl('Add').click()
    assert u'"föø" added.' == browser.message
    assert browser.FOLDER_IN_ROOT_VIEW_URL == browser.url

    # Edit
    browser.getLink('Documents').click()  # back to parent
    assert 'föø' in browser.contents
    assert browser.FOLDER_IN_ROOT_EDIT_URL == browser.getLink('Edit').url
    browser.getLink('Edit').click()
    assert 'föø' == browser.getControl('folder title').value
    assert (['kw1', 'kw3'] ==
            browser.getControl('read only access').displayValue)
    assert ['kw2'] == browser.getControl('read and write access').displayValue

    browser.getControl('folder title').value = 'bä®'
    browser.getControl('read only access').displayValue = []
    browser.getControl('read and write access').displayValue = ['kw3']
    browser.getControl('Save').click()
    assert 'Data successfully updated.' == browser.message
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.url

    # Delete
    browser.getLink('Delete').click()
    assert ('Do you really want to delete this folder and all its contents?'
            in browser.contents)
    browser.getControl('Yes').click()
    assert u'"bä®" deleted.' == browser.message
    assert 'This folder is (currently) empty.' in browser.contents


def test_folder__Add__1(address_book, FolderFactory, browser):
    """It requires unique folder titles inside the folder."""
    FolderFactory(address_book, u'foolder')
    browser.login('mgr')
    browser.open(browser.FOLDER_ADD_URL)
    browser.getControl('folder title').value = 'foolder'
    browser.getControl('Add').click()
    assert 'There were some errors.' in browser.contents
    assert ('There is already an object with this title in this folder.'
            in browser.contents)


def test_folder__Add__2(address_book, FolderFactory, browser):
    """It allows duplicate folder titles in different folders."""
    folder = FolderFactory(address_book, u'special docs')
    FolderFactory(address_book, u'foo', parent=folder)
    browser.login('mgr')
    browser.open(browser.FOLDER_ADD_URL)
    browser.getControl('folder title').value = 'foo'
    browser.getControl('Add').click()
    assert '"foo" added.' == browser.message
    assert browser.FOLDER2_IN_ROOT_VIEW_URL == browser.url


def test_folder__Edit__1(address_book, FolderFactory, browser):
    """It requires unique folder titles inside the folder."""
    FolderFactory(address_book, u'bar')
    FolderFactory(address_book, u'foo')
    browser.login('mgr')
    browser.open(browser.FOLDER_IN_ROOT_EDIT_URL)
    browser.getControl('folder title').value = 'foo'
    browser.getControl('Save').click()
    assert 'There were some errors.' in browser.contents
    assert ('There is already an object with this title in this folder.'
            in browser.contents)


def test_folder__Edit__2(address_book, FolderFactory, browser):
    """It allows duplicate folder titles in different folders."""
    FolderFactory(address_book, u'bar')
    folder = FolderFactory(address_book, u'special docs')
    FolderFactory(address_book, u'foo', parent=folder)
    browser.login('mgr')
    browser.open(browser.FOLDER_IN_ROOT_EDIT_URL)
    browser.getControl('folder title').value = 'foo'
    browser.getControl('Save').click()
    assert 'Data successfully updated.' == browser.message
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.url


def test_folder__Delete__1(
        address_book, FolderFactory, DocumentFactory, browser):
    """It renders the number of contained objects in the are-you-sure-form."""
    folder = FolderFactory(address_book, u'for delete')
    FolderFactory(address_book, u'folder outside')  # does not count
    sub = FolderFactory(address_book, u'sub folder', parent=folder)
    DocumentFactory(address_book, u'foo', u'foo.txt', parent=folder)
    DocumentFactory(address_book, u'bar', u'bar.txt', parent=sub)

    browser.login('mgr')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    browser.getLink('Delete', index=1).click()
    assert browser.FOLDER_IN_ROOT_DELETE_URL == browser.url
    assert (
        'number of objects in folder (incl. sub-folders)' in browser.contents)
    assert (
        '<span id="form-widgets-num" class="text-widget int-field">3</span>'
        in browser.contents)


def test_folder__List__1(address_book, UserFactory, browser):
    """It cannot be accessed without the `Document user` role."""
    UserFactory(address_book, u'Valter', u'Vimladil', u'vv@example.com',
                u'1qay2wsx', roles=[])

    browser.formlogin('vv@example.com', '1qay2wsx')
    assert [
        'Master data',
    ] == browser.etree.xpath('//ul[@id="main-menu"]/li/a/span/text()')

    with pytest.raises(zope.testbrowser.browser.HTTPError) as err:
        browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    assert 'HTTP Error 403: Forbidden' == str(err.value)

    assert 'You are not authorized.' in browser.contents


def test_folder__List__2(
        address_book, KeywordFactory, DocumentFactory, FolderFactory,
        UserFactory, browser):
    """It does not show content objects if the user does not have the ...

    ... required keywords.
    """
    kw_foo = KeywordFactory(address_book, u'foo')
    UserFactory(address_book, u'Valter', u'Vimladil', u'vv@example.com',
                u'1qay2wsx', roles=[u'Document user'])
    FolderFactory(address_book, u'foo docs', read_only=[kw_foo])
    DocumentFactory(address_book, u'bar', u'bar.txt')

    browser.formlogin('vv@example.com', '1qay2wsx')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    assert 'This folder is (currently) empty.' in browser.contents


def test_folder__List__3(
        address_book, KeywordFactory, FolderFactory, browser, UserFactory):
    """It shows folders where the user has a keyword of folder's r/o list."""
    kw_foo = KeywordFactory(address_book, u'foo')
    UserFactory(address_book, u'Valter', u'Vimladil', u'vv@example.com',
                u'1qay2wsx', roles=[u'Document user'], keywords=[kw_foo])
    FolderFactory(address_book, u'foo docs', read_only=[kw_foo])
    browser.formlogin('vv@example.com', '1qay2wsx')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    assert browser.FOLDER_IN_ROOT_VIEW_URL == browser.getLink('foo docs').url


def test_folder__List__4(
        address_book, KeywordFactory, FolderFactory, browser, UserFactory):
    """It shows folders where the user has a keyword of folder's r/w list."""
    kw_foo = KeywordFactory(address_book, u'foo')
    UserFactory(address_book, u'Valter', u'Vimladil', u'vv@example.com',
                u'1qay2wsx', roles=[u'Document user'], keywords=[kw_foo])
    FolderFactory(address_book, u'foo docs', read_write=[kw_foo])
    browser.formlogin('vv@example.com', '1qay2wsx')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    assert browser.FOLDER_IN_ROOT_VIEW_URL == browser.getLink('foo docs').url


def test_folder__List__5(
        address_book, KeywordFactory, FolderFactory, browser, UserFactory):
    """It shows folders where the user has r/o and r/w access."""
    kw_foo = KeywordFactory(address_book, u'foo')
    UserFactory(address_book, u'Valter', u'Vimladil', u'vv@example.com',
                u'1qay2wsx', roles=[u'Document user'], keywords=[kw_foo])
    FolderFactory(
        address_book, u'foo docs', read_only=[kw_foo], read_write=[kw_foo])
    browser.formlogin('vv@example.com', '1qay2wsx')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    assert browser.FOLDER_IN_ROOT_VIEW_URL == browser.getLink('foo docs').url


def test_folder__List__6(
        address_book, KeywordFactory, FolderFactory, browser, UserFactory):
    """It does not show folders where the user has no access."""
    kw_foo = KeywordFactory(address_book, u'foo')
    kw_bar = KeywordFactory(address_book, u'bar')
    kw_baz = KeywordFactory(address_book, u'baz')
    UserFactory(address_book, u'Valter', u'Vimladil', u'vv@example.com',
                u'1qay2wsx', roles=[u'Document user'], keywords=[kw_foo])
    FolderFactory(
        address_book, u'foo docs', read_only=[kw_baz], read_write=[kw_bar])
    browser.formlogin('vv@example.com', '1qay2wsx')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    with pytest.raises(zope.testbrowser.browser.LinkNotFoundError):
        browser.getLink('foo docs')


def test_folder__List__7(
        address_book, KeywordFactory, FolderFactory, browser, UserFactory):
    """Read rights are not inherited to sub folders but from parents.

    The latter is needed so the user can navigate to the folder he is allowed
    to read.
    """
    kw_foo = KeywordFactory(address_book, u'foo')
    kw_bar = KeywordFactory(address_book, u'bar')
    UserFactory(address_book, u'Valter', u'Vimladil', u'vv@example.com',
                u'1qay2wsx', roles=[u'Document user'], keywords=[kw_foo])
    UserFactory(address_book, u'Ben', u'Utzer', u'ben@example.com',
                u'1qay2wsx', roles=[u'Document user'], keywords=[kw_bar])
    foo = FolderFactory(
        address_book, u'foo folder', read_only=[kw_foo])
    sub = FolderFactory(
        address_book, u'sub folder', parent=foo, read_only=[kw_foo])
    FolderFactory(
        address_book, u'sub folder2', parent=foo, read_only=[kw_foo])
    FolderFactory(
        address_book, u'sub sub2 folder', parent=sub, read_only=[kw_bar])

    # Read rights are not inherited to sub folders:
    browser.formlogin('vv@example.com', '1qay2wsx')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    browser.getLink('foo folder').click()
    assert browser.FOLDER_IN_ROOT_VIEW_URL == browser.url
    assert 'sub folder2' in browser.contents
    browser.getLink('sub folder').click()
    assert 'sub sub2 folder' not in browser.contents

    browser.logout()
    # But a read right in a subfolder allows to access its parent folders.
    browser.formlogin('ben@example.com', '1qay2wsx')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    browser.getLink('foo folder').click()
    assert browser.FOLDER_IN_ROOT_VIEW_URL == browser.url
    assert 'sub folder2' not in browser.contents
    browser.getLink('sub folder').click()
    assert 'sub sub2 folder' in browser.contents


@pytest.mark.xfail
def test_folder__List__8(folders_and_users, browser):  # pragma: no cover
    """Read/write rights in a sub folder result in read rights in the parent.

    Read/Write rights are not inherited to sub folders.
    """
    # address_book = folders_and_users
    browser.formlogin('u_rw3@example.com', 'password')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    # The prerequisites for this test are not yet implemented :-(
    # That's why the test is marked as xfail and "pragma: no cover".
    browser.getLink('Top 1').click()
    browser.getLink('Sub 2').click()
    browser.getLink('Sub 2').click()
    browser.getLink('Sub 3').click()
    open('response.html', 'w').write(browser.contents)

    assert False, 'nyi'

# XXX
# * The local roles must not be inherited from a parent folder!
#   Write this in the description of the roles on IFolder, too. <- sicher?
# * IRootFolder needs role settings, too (put them into master data)
# * The roles `Document editor` and `Document visitor` should not show up
#   in the roles list when editing a user.
# * Add a view to edit the r/o and r/w keywords for the root folder in master
#   data.
