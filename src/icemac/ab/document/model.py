# -*- coding: utf-8 -*-
from icemac.addressbook.i18n import _
import grokcore.annotation as grok
import icemac.ab.document.interfaces
import icemac.addressbook.entities
import icemac.addressbook.file.file
import icemac.addressbook.interfaces
import zope.container.btree
import zope.interface


class Folder(zope.container.btree.BTreeContainer):
    """Container containing documents and/or other folders."""

    zope.interface.implements(icemac.ab.document.interfaces.IFolder)


folder_entity = icemac.addressbook.entities.create_entity(
    _(u'folder'), icemac.ab.document.interfaces.IFolder, Folder)


class Document(icemac.addressbook.file.file.File):
    """Container containing documents and/or other folders."""

    zope.interface.implements(icemac.ab.document.interfaces.IDocument)


document_entity = icemac.addressbook.entities.create_entity(
    _(u'document'), icemac.ab.document.interfaces.IDocument, Document)


@grok.adapter(icemac.addressbook.interfaces.IAddressBook)
@grok.implementer(icemac.ab.document.interfaces.IFolder)
def documents(address_book):
    """Adapt the address book to its documents container."""
    return address_book.documents
