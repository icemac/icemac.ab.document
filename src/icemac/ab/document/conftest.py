import icemac.ab.document.interfaces
import icemac.ab.document.testing
import icemac.addressbook.conftest
import icemac.addressbook.testing
import icemac.addressbook.utils
import pytest


pytest_plugins = 'icemac.addressbook.fixtures'


# Fixtures to set-up infrastructure which are usable in tests:


@pytest.yield_fixture(scope='function')
def address_book(addressBookConnectionF):
    """Get the address book with a document folder as site."""
    for address_book in icemac.addressbook.conftest.site(
            addressBookConnectionF):
        yield address_book


@pytest.fixture(scope='function')
def browser(browserWsgiAppS):
    """Fixture for testing with zope.testbrowser."""
    assert icemac.addressbook.conftest.CURRENT_CONNECTION is not None, \
        "The `browser` fixture needs a database fixture like `address_book`."
    return icemac.ab.document.testing.Browser(wsgi_app=browserWsgiAppS)


# Fixtures to create objects:


@pytest.fixture(scope='session')
def FolderFactory():
    """Create a document folder."""
    def create_folder(address_book, title, parent=None, **kw):
        if parent is None:
            parent = address_book.documents
        return icemac.addressbook.testing.create(
            address_book, parent, icemac.ab.document.interfaces.IFolder, **kw)
    return create_folder


@pytest.fixture(scope='session')
def DocumentFactory():
    """Create a document folder."""
    def create_document(address_book, title, parent=None, **kw):
        if parent is None:
            parent = address_book.documents
        return icemac.addressbook.testing.create(
            address_book, parent,
            icemac.ab.document.interfaces.IDocument, **kw)
    return create_document


# Infrastructure fixtures


@pytest.yield_fixture(scope='session')
def zcmlS():
    """Load document ZCML on session scope."""
    layer = icemac.addressbook.testing.SecondaryZCMLLayer(
        'Document', __name__, icemac.ab.document)
    layer.setUp()
    yield layer
    layer.tearDown()


@pytest.yield_fixture(scope='session')
def zodbS(zcmlS):
    """Create an empty test ZODB."""
    for zodb in icemac.addressbook.testing.pyTestEmptyZodbFixture():
        yield zodb


@pytest.yield_fixture(scope='session')
def addressBookS(zcmlS, zodbS):
    """Create an address book for the session."""
    for zodb in icemac.addressbook.conftest.pyTestAddressBookFixture(
            zodbS, 'DocumentS'):
        yield zodb


@pytest.yield_fixture(scope='function')
def addressBookConnectionF(addressBookS):
    """Get the connection to the right demo storage."""
    for connection in icemac.addressbook.conftest.pyTestStackDemoStorage(
            addressBookS, 'DocumentF'):
        yield connection
