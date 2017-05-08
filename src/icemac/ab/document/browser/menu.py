import grokcore.component as grok
import icemac.addressbook.browser.interfaces
import icemac.addressbook.browser.menus.menu
import z3c.menu.ready2go.checker
import z3c.menu.ready2go.item
import zope.interface


class DocumentsMenuItem(z3c.menu.ready2go.item.SiteMenuItem):
    """Menu item for the documents tab in the site menu."""


class DocumentsMenuItemSelectedChecker(
        z3c.menu.ready2go.checker.TrueSelectedChecker,
        grok.MultiAdapter):
    """Selected checker for the documents menu item in the site menu."""

    grok.adapts(zope.interface.Interface,
                icemac.addressbook.browser.interfaces.IAddressBookLayer,
                zope.interface.Interface,
                icemac.addressbook.browser.menus.menu.MainMenu,
                DocumentsMenuItem)

    @property
    def selected(self):
        if icemac.ab.document.interfaces.IFolder.providedBy(self.context):
            return True
        if icemac.ab.document.interfaces.IDocument.providedBy(self.context):
            return True
        return False
