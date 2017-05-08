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


class IFolder(IDocumentObject):
    """Storage for containers and documents."""


class IDocument(zope.interface.Interface):
    """Document storing binary data."""
