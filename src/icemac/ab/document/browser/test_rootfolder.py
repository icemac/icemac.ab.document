from zope.testbrowser.browser import HTTPError
import pytest


def test_rootfolder__NotFound__1(address_book, browser):
    """There is no edit view for the root folder."""
    browser.login('mgr')
    with pytest.raises(HTTPError) as err:
        browser.open(browser.ROOT_FOLDER_EDIT_URL)
    assert 'HTTP Error 404: Not Found' == str(err.value)


def test_rootfolder__NotFound__2(address_book, browser):
    """There is no delete view for the root folder."""
    browser.login('mgr')
    with pytest.raises(HTTPError) as err:
        browser.open(browser.ROOT_FOLDER_DELETE_URL)
    assert 'HTTP Error 404: Not Found' == str(err.value)
