# -*- coding: utf-8 -*-
def test_folder__Add__List__Edit__Delete__1(address_book, browser):
    """They allow to CRUD a new folder."""
    browser.login('mgr')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)

    # Add
    browser.getLink('folder').click()
    assert browser.FOLDER_ADD_URL == browser.url
    browser.getControl('folder title').value = 'föø'
    browser.getControl('Add').click()
    assert u'"föø" added.' == browser.message
    assert browser.FOLDER_IN_ROOT_VIEW_URL == browser.url

    # Edit
    browser.getLink('Documents').click()  # back to parent
    assert 'föø' in browser.contents
    assert browser.FOLDER_IN_ROOT_EDIT_URL == browser.getLink('Edit').url
    browser.getLink('Edit').click()
    assert 'föø' == browser.getControl('folder title').value
    browser.getControl('folder title').value = 'bä®'
    browser.getControl('Apply').click()
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
    browser.getControl('Apply').click()
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
    browser.getControl('Apply').click()
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
