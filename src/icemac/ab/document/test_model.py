from icemac.ab.document.model import Document
from icemac.ab.document.model import Folder
from icemac.ab.document.model import FolderPrincipalRoleMap
from icemac.ab.document.model import RootFolder
from zope.interface.verify import verifyObject
import icemac.ab.document.interfaces
import pytest
import zope.securitypolicy.interfaces


def test_model__RootFolder__1(zcmlS):
    """It actually implements `IRootFolder`."""
    assert verifyObject(
        icemac.ab.document.interfaces.IRootFolder,
        RootFolder())


def test_model__Folder__1(zcmlS):
    """It actually implements `IFolder`."""
    assert verifyObject(
        icemac.ab.document.interfaces.IFolder,
        Folder())


def test_model__Document__1(zcmlS):
    """It actually implements `IDocument`."""
    assert verifyObject(
        icemac.ab.document.interfaces.IDocument,
        Document())


def test_model__FolderPrincipalRoleMap__1(zcmlS):
    """It actually implements `IPrincipalRoleMap`."""
    assert verifyObject(
        zope.securitypolicy.interfaces.IPrincipalRoleMap,
        FolderPrincipalRoleMap(None))


@pytest.mark.parametrize('method_name, args', [
    ('getPrincipalsForRole', (None,)),
    ('getSetting', (None, None)),
    ('getPrincipalsAndRoles', ()),
])
def test_model__FolderPrincipalRoleMap__2(method_name, args):
    """Some methods are not needed, so they are not implemented."""
    fprm = FolderPrincipalRoleMap(None)
    with pytest.raises(NotImplementedError):
        getattr(fprm, method_name)(*args)
