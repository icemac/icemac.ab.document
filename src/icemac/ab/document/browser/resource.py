from icemac.addressbook.browser.resource import base_css
import fanstatic
import icemac.ab.document.browser.interfaces
import icemac.addressbook.browser.favicon
import zope.viewlet.viewlet


lib = fanstatic.Library('document', 'resources')
document_css = fanstatic.Resource(lib, 'document.css', depends=[base_css])
document_js = fanstatic.Resource(
    lib, 'document.js', depends=[],
    bottom=True)


class DocumentResources(zope.viewlet.viewlet.ViewletBase):
    """Resources which are needed for the documents."""

    def update(self):
        document_css.need()
        document_js.need()

    def render(self):
        return u''


def set_layer(context, request):
    """Set the document layer on the request, so the resources are rendered."""
    zope.interface.alsoProvides(
        request, icemac.ab.document.browser.interfaces.IDocumentLayer)


document_favicon = icemac.addressbook.browser.favicon.FavIconData(
    '/fanstatic/document/img/favicon.ico',
    '/fanstatic/document/img/favicon-preview.png')
