# -*- coding: utf-8 -*-
import os.path
import setuptools


def read(*path_elements):
    """Read file."""
    return open(os.path.join(*path_elements)).read()


version = '0.1.dev0'
long_description = '\n\n'.join([
    read('README.rst'),
    read('CHANGES.rst'),
])

setuptools.setup(
    name='icemac.ab.document',
    version=version,
    description="Document storage feature for icemac.addressbook",
    long_description=long_description,
    keywords='icemac addressbook document storage download groups',
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    download_url='https://pypi.org/project/icemac.ab.document',
    url='https://bitbucket.org/icemac/icemac.ab.document',
    license='MIT',
    classifiers=[
        'Development Status :: :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Paste',
        'Framework :: Zope3',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac', 'icemac.ab'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grokcore.annotation',
        'icemac.addressbook >= 9.0.dev0',
        'setuptools',
    ],
    extras_require=dict(
        test=[
            'icemac.addressbook [test]',
        ]),
    entry_points="""
      [fanstatic.libraries]
      document = icemac.ab.document.browser.resource:lib
      """,
)
