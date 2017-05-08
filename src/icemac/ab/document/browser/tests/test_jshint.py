import icemac.addressbook.testing


class JSLintTest(icemac.addressbook.testing.JSLintTest):
    """Lint JS files."""

    include = (
        'icemac.ab.document.browser:resources',
    )
