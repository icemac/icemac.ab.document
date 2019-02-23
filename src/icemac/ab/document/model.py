# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import grokcore.component as grok
import icemac.ab.document.interfaces
import icemac.addressbook.entities
import icemac.addressbook.file.file
import icemac.addressbook.interfaces
import icemac.addressbook.utils
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
        icemac.ab.document.interfaces.IFolder)


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
