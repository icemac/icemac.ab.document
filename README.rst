This package provides a document storage feature for `icemac.addressbook`_.

.. _`icemac.addressbook` : https://pypi.org/project/icemac.addressbook/

Copyright (c) 2017-2020 Michael Howitz

This package is licensed under the MIT License, see LICENSE.txt inside the
package.

.. contents::

=========
 Hacking
=========

Source code
===========

Get the source code::

   $ git clone https://github.com/icemac/icemac.ab.document

or fork me at: https://github.com/icemac/icemac.ab.document

Running the tests
=================

To run the tests yourself call::

  $ virtualenv-2.7 .
  $ bin/pip install zc.buildout
  $ bin/buildout -n
  $ bin/py.test
