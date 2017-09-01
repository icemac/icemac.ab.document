import icemac.ab.document.interfaces
import icemac.ab.document.model
import icemac.addressbook.addressbook
import zope.component
import zope.component.hooks


@zope.component.adapter(
    icemac.addressbook.addressbook.AddressBookCreated)
def install_documents(event):
    """Install the documents in the newly created addressbook."""
    address_book = event.address_book
    with zope.component.hooks.site(address_book):
        icemac.addressbook.addressbook.create_and_register(
            address_book, 'documents', icemac.ab.document.model.RootFolder,
            icemac.ab.document.interfaces.IRootFolder)
        update_documents_infrastructure(address_book)


def update_documents_infrastructure(address_book):
    """Update the documents infrastructure to install new components."""
    with zope.component.hooks.site(address_book):
        icemac.addressbook.addressbook.add_entity_to_order(
            address_book.orders, icemac.ab.document.interfaces.IDocument)
        icemac.addressbook.addressbook.add_entity_to_order(
            address_book.orders, icemac.ab.document.interfaces.IFolder)
