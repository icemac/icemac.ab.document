# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import icemac.ab.document.interfaces
import icemac.addressbook.entities
import icemac.addressbook.file.file
import icemac.addressbook.interfaces
import zope.container.btree
import zope.interface
import zope.schema.fieldproperty


@zope.interface.implementer(
    icemac.ab.document.interfaces.IRootFolder,
    icemac.ab.document.interfaces.IFolder)
class RootFolder(zope.container.btree.BTreeContainer):
    """Top level container for documents and/or folders."""

    zope.schema.fieldproperty.createFieldProperties(
        icemac.ab.document.interfaces.IFolder)


@zope.interface.implementer(
    icemac.ab.document.interfaces.IFolder)
class Folder(zope.container.btree.BTreeContainer):
    """Container containing documents and/or other folders."""

    zope.schema.fieldproperty.createFieldProperties(
        icemac.ab.document.interfaces.IFolder)


folder_entity = icemac.addressbook.entities.create_entity(
    _(u'folder'), icemac.ab.document.interfaces.IFolder, Folder)


@zope.interface.implementer(
    icemac.ab.document.interfaces.IDocument)
class Document(icemac.addressbook.file.file.File):
    """Container containing documents and/or other folders."""

    zope.schema.fieldproperty.createFieldProperties(
        icemac.ab.document.interfaces.IDocument,
        omit=['data', 'size'])


document_entity = icemac.addressbook.entities.create_entity(
    _(u'document'), icemac.ab.document.interfaces.IDocument, Document)
