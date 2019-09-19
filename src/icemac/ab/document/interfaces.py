from icemac.addressbook.i18n import _
import gocept.reference.field
import icemac.addressbook.file.interfaces
import icemac.addressbook.interfaces
import icemac.addressbook.utils
import zope.interface
import zope.schema

PACKAGE_ID = 'icemac.ab.document'


class IDocumentsProvider(zope.interface.Interface):
    """Marker interface for objects providing documents on an attribute.

    This is necessary to meet security which otherwise raises a ForbiddenError.

    """

    documents = zope.interface.Attribute(u'IFolder')


class IDocumentObject(zope.interface.Interface):
    """Marker interface for objects belonging to the documents package.

    This is needed to get the documents skin layer during traversal.

    """


class IFolderish(zope.interface.Interface):
    """Marker interface for objects which behave like folders."""


class IRootFolder(IDocumentObject,
                  IFolderish):
    """Top level storage for folders and documents."""


class IFolder(IDocumentObject,
              IFolderish):
    """Storage for containers and documents."""

    title = zope.schema.TextLine(
        title=_(u'folder title'),
        description=_(u'Name which is shown in the list view.'))

    read_only = gocept.reference.field.Set(
        title=_('read only access'),
        description=_(
            'Persons with at least one of the selected keywords have read'
            ' only access in this folder.'),
        required=False,
        value_type=zope.schema.Choice(
            title=_('keywords'),
            source=icemac.addressbook.interfaces.keyword_source))

    read_write = gocept.reference.field.Set(
        title=_('read and write access'),
        description=_(
            'Persons with at least one of the selected keywords have read'
            ' and write access in this folder.'),
        required=False,
        value_type=zope.schema.Choice(
            title=_('keywords'),
            source=icemac.addressbook.interfaces.keyword_source))


class IDocumentBase(icemac.addressbook.file.interfaces.IFile):
    """Base class for IDocument.

    Needed for copying the schema field so we do not get the customizations of
    IFile.
    """


# Copy schema fields, reason see above.
icemac.addressbook.utils.copy_schema_fields(
    icemac.addressbook.file.interfaces.IFile, IDocumentBase)


class IDocument(IDocumentBase):
    """Document storing binary data."""

    title = zope.schema.TextLine(
        title=_(u'document title'),
        description=_(u'Name which is shown in the list view.'))


IDocument['title'].order = -1
