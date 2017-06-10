from __future__ import unicode_literals
import pytest


@pytest.fixture(scope='function')
def document_menu(address_book, browser, sitemenu):
    """Fixture to test the document menu."""
    browser.login('mgr')
    return sitemenu(browser, 2, 'Documents', browser.DOCUMENTS_OVERVIEW_URL)


def test_menu__document_menu__1(document_menu):
    """Asserting that the menu with the index 2 is `Documents`."""
    document_menu.assert_correct_menu_item_is_tested()


def test_menu__document_menu__2(document_menu):
    """The documents tab is selected on the documents overview."""
    assert document_menu.item_selected(document_menu.menu_item_URL)


def test_menu__document_menu__3(document_menu):
    """The documents tab is not selected on master data."""
    assert not document_menu.item_selected(
        document_menu.browser.MASTER_DATA_URL)


def test_menu__document_menu__4(address_book, document_menu, DocumentFactory):
    """The documents tab is not selected on a document."""
    DocumentFactory(address_book, 'foo.doc', 'foo doc')
    # document_menu.browser.handleErrors = False
    assert document_menu.item_selected(
        document_menu.browser.DOCUMENT_IN_ROOT_EDIT_URL)


def test_menu__document_menu__5(address_book, document_menu, FolderFactory):
    """The documents tab is not selected on a folder."""
    FolderFactory(address_book, 'foo folder')
    assert document_menu.item_selected(
        document_menu.browser.FOLDER_IN_ROOT_VIEW_URL)


def test_menu__DocumentMenuItem__1(address_book, browser):
    """It allows to navigate the to calendar.

    The calendar view defaults to the month overview.
    """
    browser.login('mgr')
    browser.open(browser.ADDRESS_BOOK_DEFAULT_URL)
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.getLink('Documents').url
    browser.getLink('Documents').click()
    assert browser.DOCUMENTS_OVERVIEW_URL == browser.url
