import icemac.addressbook.testing


class Browser(icemac.addressbook.testing.Browser):
    """Browser adapted for documents."""

    BASE = 'http://localhost/ab/'
    DOCUMENTS_OVERVIEW_URL = BASE + '++attribute++documents'
    DOCUMENTS_INDEX_URL = BASE + '++attribute++documents/@@index.html'

    DOCUMENT_ADD_URL = BASE + '++attribute++documents/@@addDocument.html'
    DOCUMENT_IN_ROOT_DOWNLOAD_URL = BASE + '++attribute++documents/Document'
    DOCUMENT_IN_ROOT_EDIT_URL = BASE + (
        '++attribute++documents/Document/@@edit.html')
    FOLDER_IN_ROOT_VIEW_URL = BASE + '++attribute++documents/Folder'


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
