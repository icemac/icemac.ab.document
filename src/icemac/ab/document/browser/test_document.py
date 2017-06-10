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
    browser.getControl('Apply').click()
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
    assert (
        'This folder does not (yet) contain any documents.' in
        browser.contents)
