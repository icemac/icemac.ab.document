from icemac.addressbook.i18n import _
import icemac.ab.document.interfaces
import icemac.addressbook.browser.table
import z3c.table.column


class DocumentsList(icemac.addressbook.browser.table.Table):
    """List the documents in the folder."""

    no_rows_message = _('This folder does not (yet) contain any documents.')

    def setUpColumns(self):
        return [
            z3c.table.column.addColumn(
                self, icemac.addressbook.browser.table.TitleLinkColumn,
                'title', weight=10, header=_(u'files'), attrName='name'),
            z3c.table.column.addColumn(
                self, icemac.addressbook.browser.table.LinkColumn, 'edit',
                header=_(u''), weight=90, linkContent=_(u'Edit'),
                linkName='edit.html'),
            z3c.table.column.addColumn(
                self, icemac.addressbook.browser.table.DeleteLinkColumn,
                'delete', weight=20),
        ]

    @property
    def values(self):
        objs = icemac.addressbook.utils.iter_by_interface(
            self.context, icemac.ab.document.interfaces.IDocument)
        for obj in objs:
            yield obj
