import pytest


# @pytest.mark.parametrize('username,url', [
#     ('cal-visitor', 'CALENDAR_MONTH_OVERVIEW_URL'),
#     ('cal-editor', 'EVENT_ADD_URL')])
# def test_resource__1(address_book, browser, username, url):
#     """The `document.css` is rendered on document pages."""
#     browser.login(username)
#     browser.open(getattr(browser, url))
#     assert 'href="/fanstatic/document/:version:' in browser.contents
#     assert 'document.css' in browser.contents
