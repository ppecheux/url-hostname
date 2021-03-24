from url_hostname.host import Host


def test_str():
    h = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert str(h) == "wikipedia.org"


def test_repr():
    h = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert repr(h) == "Host('wikipedia.org')"


def test_subdomains_str():
    h = Host.build(
        subdomains=("docs", "aws"),
        second_level_domain="amazon",
        top_level_domain="com",
    )
    assert str(h) == "docs.aws.amazon.com"

def test_domain_name():
    h = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert h.domain_name == "wikipedia.org"    

def test_leaf():
    h = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert h.leaf == "wikipedia"


def test_subdomains_leaf():
    h = Host.build(
        subdomains=("docs", "aws"),
        second_level_domain="amazon",
        top_level_domain="com",
    )
    assert h.leaf == "docs"

def test_with_leaf():
    h = Host.build(
        subdomains="en",
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    h = h.with_leaf("fr")
    assert str(h) == "fr.wikipedia.org"

def test_with_subdomains():
    h = Host.build(
        subdomains="en",
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    assert str(h.with_subdomains("fr")) == "fr.wikipedia.org"

def test_relative_to_1_host():
    h0 = Host.build(
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    h1 = h0.with_leaf("wikipedia")
    assert str(h0.relative_to(h1)) ==  "wikipedia.org"
