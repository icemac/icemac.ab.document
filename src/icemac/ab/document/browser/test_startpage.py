import pytest


@pytest.mark.webdriver
def test_startpage__documents__1(address_book, webdriver):
    """It redirects to the documents if this is set on the address book."""
    ab = webdriver.address_book
    webdriver.login('mgr', ab.ADDRESS_BOOK_EDIT_URL)
    ab.startpage = 'Documents'
    ab.submit('apply')
    webdriver.open(ab.ADDRESS_BOOK_DEFAULT_URL)
    assert webdriver.documents.DOCUMENTS_INDEX_URL == webdriver.path
