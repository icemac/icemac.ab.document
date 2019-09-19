# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import gocept.reference
import grokcore.component as grok
import icemac.ab.document.interfaces
import icemac.addressbook.entities
import icemac.addressbook.file.file
import icemac.addressbook.interfaces
import icemac.addressbook.utils
import itertools
import zope.authentication.interfaces
import zope.component
import zope.container.btree
import zope.interface
import zope.schema.fieldproperty


@zope.interface.implementer(icemac.ab.document.interfaces.IRootFolder)
class RootFolder(zope.container.btree.BTreeContainer):
    """Top level container for documents and/or folders.

    This class must not implement `IFolder` as this causes too many
    interferences in places where this object should behave differently from
    `IFolder`.
    """

    zope.schema.fieldproperty.createFieldProperties(
        icemac.ab.document.interfaces.IRootFolder)


@grok.adapter(icemac.ab.document.interfaces.IDocumentsProvider)
@grok.implementer(icemac.ab.document.interfaces.IRootFolder)
def documents_for_address_book(context):
    """Get the documents root folder of an address book."""
    return context.documents


@zope.interface.implementer(
    icemac.ab.document.interfaces.IFolder,
    icemac.addressbook.interfaces.IMayHaveCustomizedPredfinedFields)
class Folder(zope.container.btree.BTreeContainer):
    """Container containing documents and/or other folders."""

    zope.schema.fieldproperty.createFieldProperties(
        icemac.ab.document.interfaces.IFolder,
        omit=['read_only', 'read_write'])

    read_only = gocept.reference.ReferenceCollection(
        'read_only', ensure_integrity=True)

    read_write = gocept.reference.ReferenceCollection(
        'read_write', ensure_integrity=True)

    def __init__(self, *args, **kw):
        super(Folder, self).__init__(*args, **kw)
        self.read_only = set()
        self.read_write = set()


folder_entity = icemac.addressbook.entities.create_entity(
    _(u'folder'), icemac.ab.document.interfaces.IFolder, Folder)


@zope.interface.implementer(
    icemac.ab.document.interfaces.IDocument,
    icemac.addressbook.interfaces.IMayHaveCustomizedPredfinedFields)
class Document(icemac.addressbook.file.file.BaseFile):
    """Container containing documents and/or other folders."""

    zope.schema.fieldproperty.createFieldProperties(
        icemac.ab.document.interfaces.IDocument,
        omit=['data', 'size'])


document_entity = icemac.addressbook.entities.create_entity(
    _(u'document'), icemac.ab.document.interfaces.IDocument, Document)
unique_titles = icemac.addressbook.utils.unique_by_attr_factory(
    'title', _(u'There is already an object with this title in this folder.'))


class FolderPrincipalRoleMap(grok.Adapter):
    """Roles for a principal on a folder depending on their keywords."""

    grok.context(icemac.ab.document.interfaces.IFolder)
    grok.implements(zope.securitypolicy.interfaces.IPrincipalRoleMap)

    def getPrincipalsForRole(self, role_id):
        """Get the principals that have been granted a role."""
        raise NotImplementedError()

    def getRolesForPrincipal(self, principal_id):
        """Get the roles granted to a principal."""
        principal_folder = zope.component.getUtility(
            zope.pluggableauth.interfaces.IAuthenticatorPlugin,
            name=u'icemac.addressbook.principals')
        try:
            principal = principal_folder[principal_id]
        except KeyError:
            keywords = set()
        else:
            keywords = set(principal.person.keywords)

        roles = []
        if keywords.intersection(self.context.read_only):
            setting = zope.securitypolicy.interfaces.Allow
        else:
            subfolder_keywords = itertools.chain(
                *self._keywords_of_subfolders(self.context))
            if keywords.intersection(subfolder_keywords):
                setting = zope.securitypolicy.interfaces.Allow
            else:
                setting = zope.securitypolicy.interfaces.Deny
        roles.append((u'icemac.ab.document.Visitor', setting))

        if keywords.intersection(self.context.read_write):
            roles.append((u'icemac.ab.document.Editor',
                          zope.securitypolicy.interfaces.Allow))
        return roles

    def _keywords_of_subfolders(self, parent):
        """Generator containing sets of keywords of the subfolders."""
        for folder in icemac.addressbook.utils.iter_by_interface(
                parent, icemac.ab.document.interfaces.IFolder):
            yield set(folder.read_only)
            # XXX `yield from` would be nice!
            for keywords in self._keywords_of_subfolders(folder):
                yield keywords

    def getSetting(self, role_id, principal_id, default=None):
        """Return the setting for this principal, role combination."""
        raise NotImplementedError()

    def getPrincipalsAndRoles(self):
        """Get all settings."""
        raise NotImplementedError()
