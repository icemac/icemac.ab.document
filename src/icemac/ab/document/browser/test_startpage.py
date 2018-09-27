def test_startpage__documents__2(address_book, browser):
    """It redirects to the documents if this is set on the address book."""
    browser.login('mgr')
    browser.open(browser.ADDRESS_BOOK_EDIT_URL)
    browser.getControl('start page after log-in').displayValue = 'Documents'
    browser.select_favicon()
    browser.getControl('Save').click()
    assert 'Data successfully updated.' == browser.message
    browser.open(browser.ADDRESS_BOOK_DEFAULT_URL)
    assert browser.DOCUMENTS_INDEX_URL == browser.url
