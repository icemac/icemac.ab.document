import zope.publisher.interfaces


class NotFound(object):
    """The root folder cannot be edited or deleted.

    This view exists so the corresponding views of IFolder are _not_ rendered.
    """

    def __call__(self):
        raise zope.publisher.interfaces.NotFound(self.context, self.__name__)
