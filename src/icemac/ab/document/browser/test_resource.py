import pytest


@pytest.mark.parametrize('username,url', [
    ('doc-user', 'DOCUMENTS_INDEX_URL'),
])
def test_resource__1(address_book, browser, username, url):
    """The `document.css` is rendered on document pages."""
    browser.login(username)
    browser.open(getattr(browser, url))
    assert 'href="/fanstatic/document/:version:' in browser.contents
    assert 'document.css' in browser.contents
