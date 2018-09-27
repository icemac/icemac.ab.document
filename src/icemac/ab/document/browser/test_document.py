def assert_download_file(browser, filename):
    """Assert the contents and headers of a download."""
    assert not browser.isHtml
    assert 'text/plain' == browser.headers['content-type']
    assert browser.headers[
        'content-disposition'] == 'attachment; filename=' + filename
    assert 'File contents' == browser.contents
    assert '13' == browser.headers['content-length']


def test_document__Add__Download__Edit__Delete__1(
        address_book, tmpfile, browser):
    """They allow to CRUD a new document."""
    browser.login('mgr')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)

    # Add
    browser.getLink('document').click()
    assert browser.DOCUMENT_ADD_URL == browser.url
    fh, filename = tmpfile('File contents', '.txt')
    browser.getControl('document title').value = 'foo'
    browser.getControl('file').add_file(fh, 'text/plain', filename)
    browser.getControl('Add').click()
    assert '"foo" added.' == browser.message
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.url

    # Download
    # The title link on the list view allows to download the file:
    assert browser.DOCUMENT_IN_ROOT_DOWNLOAD_URL == browser.getLink('foo').url
    browser.getLink('foo').click()
    assert_download_file(browser, filename)

    # Edit
    browser.goBack()
    assert browser.DOCUMENT_IN_ROOT_EDIT_URL == browser.getLink('Edit').url
    browser.getLink('Edit').click()

    # The new file is shown there including a widget displaying the
    # normalized name and mime type:
    assert browser.getControl('file name').value == filename
    assert 'text/plain' == browser.getControl('Mime Type').value
    # But there is no file displayed:
    assert browser.getControl('file', index=1).value is None
    # There is also a download link for the file:
    browser.getLink('Download file').click()
    assert_download_file(browser, filename)
    browser.goBack()
    # Field values can be changed:
    browser.getControl('document title').value = 'bar'
    browser.getControl('file name').value = 'bar.txt'
    browser.getControl('Save').click()
    assert 'Data successfully updated.' == browser.message

    # Download
    browser.getLink('bar').click()
    assert_download_file(browser, 'bar.txt')
    browser.goBack()

    # Delete
    browser.getLink('Delete').click()
    assert 'Do you really want to delete this document?' in browser.contents
    browser.getControl('Yes').click()
    assert '"bar" deleted.' == browser.message
    assert 'This folder is (currently) empty.' in browser.contents


def test_document__Add__1(address_book, tmpfile, DocumentFactory, browser):
    """It requires unique document titles inside the folder."""
    DocumentFactory(address_book, u'foo.txt', u'foo')
    browser.login('mgr')
    browser.open(browser.DOCUMENT_ADD_URL)
    fh, filename = tmpfile('File contents', '.txt')
    browser.getControl('document title').value = 'foo'
    browser.getControl('file').add_file(fh, 'text/plain', filename)
    browser.getControl('Add').click()
    assert 'There were some errors.' in browser.contents
    assert ('There is already an object with this title in this folder.'
            in browser.contents)


def test_document__Add__2(
        address_book, tmpfile, FolderFactory, DocumentFactory, browser):
    """It allows duplicate document titles in different folders."""
    folder = FolderFactory(address_book, u'special docs')
    DocumentFactory(address_book, u'foo.txt', u'foo', parent=folder)
    browser.login('mgr')
    browser.open(browser.DOCUMENT_ADD_URL)
    fh, filename = tmpfile('File contents', '.txt')
    browser.getControl('document title').value = 'foo'
    browser.getControl('file').add_file(fh, 'text/plain', filename)
    browser.getControl('Add').click()
    assert '"foo" added.' == browser.message
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.url


def test_document__Edit__1(address_book, DocumentFactory, browser):
    """It requires unique document titles inside the folder."""
    DocumentFactory(address_book, u'bar.txt', u'bar')
    DocumentFactory(address_book, u'foo.txt', u'foo')
    browser.login('mgr')
    browser.open(browser.DOCUMENT_IN_ROOT_EDIT_URL)
    browser.getControl('document title').value = 'foo'
    browser.getControl('Save').click()
    assert 'There were some errors.' in browser.contents
    assert ('There is already an object with this title in this folder.'
            in browser.contents)


def test_document__Edit__2(
        address_book, FolderFactory, DocumentFactory, browser):
    """It allows duplicate document titles in different folders."""
    DocumentFactory(address_book, u'foo.txt', u'bar')
    folder = FolderFactory(address_book, u'special docs')
    DocumentFactory(address_book, u'foo.txt', u'foo', parent=folder)
    browser.login('mgr')
    browser.open(browser.DOCUMENT_IN_ROOT_EDIT_URL)
    browser.getControl('document title').value = 'foo'
    browser.getControl('Save').click()
    assert 'Data successfully updated.' == browser.message
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.url


def test_document__Delete__1(address_book, DocumentFactory, browser):
    """It allows to cancel deleting of a document."""
    DocumentFactory(address_book, u'foo.txt', u'bar')
    browser.login('mgr')
    browser.open(browser.DOCUMENTS_OVERVIEW_URL)
    browser.getLink('Delete').click()
    assert browser.DOCUMENT_IN_ROOT_DELETE_URL == browser.url
    browser.getControl('No, cancel').click()
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.url
