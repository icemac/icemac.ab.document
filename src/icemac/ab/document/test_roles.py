from icemac.addressbook.principals.roles import has_visitor_role


def test_roles__visitor_role__1(zcmlS):
    """The document user role is registered as a visitor role."""
    assert has_visitor_role(['icemac.ab.document.User'])
