from icemac.addressbook.i18n import _
import grokcore.component as grok
import icemac.ab.document.model
import icemac.addressbook.browser.breadcrumb


class DocumentsBreadCrumb(icemac.addressbook.browser.breadcrumb.Breadcrumb):
    """Breadcrumb for the documents."""

    grok.adapts(
        icemac.ab.document.model.RootFolder,
        icemac.addressbook.browser.interfaces.IAddressBookLayer)

    title = _('Documents')
