from icemac.addressbook.i18n import _
import grokcore.component as grok
import icemac.ab.document.interfaces
import icemac.addressbook.browser.breadcrumb
import icemac.addressbook.browser.table
import z3c.table.column
import zope.schema


class List(icemac.addressbook.browser.table.Table):
    """List the contents of a folder.

    Also used for the root folder.
    """

    title = icemac.addressbook.browser.breadcrumb.DO_NOT_SHOW
    no_rows_message = _('This folder is (currently) empty.')

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
        return self.context.values()


class Add(icemac.addressbook.browser.base.BaseAddForm):
    """Add a folder."""

    title = _(u'Add new folder')
    interface = icemac.ab.document.interfaces.IFolder
    class_ = icemac.ab.document.model.Folder
    next_url = 'object'


class Edit(icemac.addressbook.browser.base.BaseEditForm):
    """Edit a folder."""

    interface = icemac.ab.document.interfaces.IFolder
    next_url = 'parent'
    title = _('Edit folder')


class IFolderDeleteFields(icemac.ab.document.interfaces.IFolder):
    """Fields to be rendered on the Delete confirm form."""

    num = zope.schema.Int(
        title=_('number of objects in folder (incl. sub-folders)'))


class FolderDeleteFields(grok.Adapter):
    """Adapter from IFolder to IFolderDeleteFields."""

    grok.context(icemac.ab.document.interfaces.IFolder)
    grok.implements(IFolderDeleteFields)

    def __init__(self, context):
        super(FolderDeleteFields, self).__init__(context)
        self.title = self.context.title
        self.num = self._count_contents(self.context)

    def _count_contents(self, parent):
        num = 0
        for i in parent.values():
            if icemac.ab.document.interfaces.IFolder.providedBy(i):
                num += self._count_contents(i)
            num += 1
        return num


class Delete(icemac.addressbook.browser.base.BaseDeleteForm):
    """Are you sure question for deleting a folder."""

    next_url = 'parent'
    next_url_after_cancel = 'parent'
    title = _('Delete folder')
    label = _('Do you really want to delete this folder and all its contents?')
    interface = IFolderDeleteFields
