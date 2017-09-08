from icemac.addressbook.i18n import _
import icemac.addressbook.file.interfaces
import zope.interface


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


class IDocument(icemac.addressbook.file.interfaces.IFile):
    """Document storing binary data."""

    title = zope.schema.TextLine(
        title=_(u'document title'),
        description=_(u'Name which is shown in the list view.'))


IDocument['title'].order = -1
