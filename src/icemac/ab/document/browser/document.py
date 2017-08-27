from icemac.addressbook.i18n import _
import icemac.ab.document.model
import icemac.addressbook.browser.base
import icemac.ab.document.interfaces


class Add(icemac.addressbook.browser.file.file.Add):
    """Add a document."""

    title = _(u'Add new document')
    interface = icemac.ab.document.interfaces.IDocument
    class_ = icemac.ab.document.model.Document


class Edit(icemac.addressbook.browser.base.BaseEditForm):
    """Edit a document."""

    interface = icemac.ab.document.interfaces.IDocument
    next_url = 'parent'
    title = _('Edit document')

    def applyChanges(self, data):
        changes = super(Edit, self).applyChanges(data)
        icemac.addressbook.browser.file.file.update_blob(
            self.widgets['data'], self.context)
        return changes


class Delete(icemac.addressbook.browser.base.BaseDeleteForm):
    """Are you sure question for deleting a document."""

    next_url = 'parent'
    next_url_after_cancel = 'parent'
    title = _('Delete document')
    label = _('Do you really want to delete this document?')
    interface = icemac.ab.document.interfaces.IDocument
    field_names = ('title', 'name')
