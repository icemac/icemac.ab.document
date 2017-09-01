import icemac.addressbook.testing


class Browser(icemac.addressbook.testing.Browser):
    """Browser adapted for documents."""

    BASE = 'http://localhost/ab/++attribute++documents'
    DOCUMENTS_OVERVIEW_URL = BASE
    DOCUMENTS_INDEX_URL = BASE + '/@@index.html'

    DOCUMENT_ADD_URL = BASE + '/@@addDocument.html'
    DOCUMENT_IN_ROOT_DOWNLOAD_URL = BASE + '/Document'
    DOCUMENT_IN_ROOT_EDIT_URL = BASE + '/Document/@@edit.html'
    DOCUMENT_IN_ROOT_DELETE_URL = BASE + '/Document/@@delete.html'

    ROOT_FOLDER_EDIT_URL = BASE + '/@@edit.html'
    ROOT_FOLDER_DELETE_URL = BASE + '/@@delete.html'

    FOLDER_ADD_URL = BASE + '/@@addFolder.html'
    FOLDER_IN_ROOT_VIEW_URL = BASE + '/Folder'
    FOLDER2_IN_ROOT_VIEW_URL = BASE + '/Folder-2'
    FOLDER_IN_ROOT_EDIT_URL = BASE + '/Folder/@@edit.html'
    FOLDER_IN_ROOT_DELETE_URL = BASE + '/Folder/@@delete.html'


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
