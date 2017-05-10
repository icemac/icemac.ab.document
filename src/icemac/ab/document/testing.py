import icemac.addressbook.testing


class Browser(icemac.addressbook.testing.Browser):
    """Browser adapted for documents."""

    BASE = 'http://localhost/ab/'
    DOCUMENTS_OVERVIEW_URL = BASE + '++attribute++documents'
    DOCUMENTS_INDEX_URL = BASE + '++attribute++documents/@@index.html'

    DOCUMENT_IN_ROOT_VIEW_URL = BASE + '++attribute++documents/Document'


class DocumentWebdriverPageObjectBase(
        icemac.addressbook.testing.WebdriverPageObjectBase):
    """Base for page object classes to used with to ``Webdriver.attach()``."""

    browser = Browser


class PODocuments(DocumentWebdriverPageObjectBase):
    """Webdriver page object for the calendar itself."""

    paths = [
        'DOCUMENTS_INDEX_URL',
    ]


icemac.addressbook.testing.Webdriver.attach(PODocuments, 'documents')
