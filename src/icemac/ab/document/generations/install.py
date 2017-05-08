# -*- coding: utf-8 -*-
import icemac.ab.document.install
import icemac.addressbook.addressbook
import icemac.addressbook.generations.utils


@icemac.addressbook.generations.utils.evolve_addressbooks
def evolve(address_book):
    """Install the documents into each existing address book."""
    icemac.ab.document.install.install_documents(
        icemac.addressbook.addressbook.AddressBookCreated(address_book))
