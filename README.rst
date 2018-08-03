This package provides a document storage feature for `icemac.addressbook`_.

.. _`icemac.addressbook` : https://pypi.org/project/icemac.addressbook/

Copyright (c) 2017-2018 Michael Howitz

This package is licensed under the MIT License, see LICENSE.txt inside the
package.

.. contents::

=========
 Hacking
=========

Source code
===========

Get the source code::

   $ hg clone https://bitbucket.org/icemac/icemac.ab.document

or fork me on: https://bitbucket.org/icemac/icemac.ab.document

Running the tests
=================

To run the tests yourself call::

  $ python2.7 bootstrap.py
  $ bin/buildout -n
  $ bin/py.test
