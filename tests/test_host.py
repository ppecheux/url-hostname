from url_hostname.host import Host


def test_str():
    host = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert str(host) == "wikipedia.org"


def test_repr():
    host = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert repr(host) == "Host('wikipedia.org')"


def test_subdomains_str():
    host = Host.build(
        subdomains=("docs", "aws"),
        second_level_domain="amazon",
        top_level_domain="com",
    )
    assert str(host) == "docs.aws.amazon.com"

def test_domain_name():
    host = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert host.domain_name == "wikipedia.org"

def test_leaf():
    host = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert host.leaf == "wikipedia"


def test_subdomains_leaf():
    host = Host.build(
        subdomains=("docs", "aws"),
        second_level_domain="amazon",
        top_level_domain="com",
    )
    assert host.leaf == "docs"

def test_with_leaf():
    host = Host.build(
        subdomains="en",
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    host = host.with_leaf("fr")
    assert str(host) == "fr.wikipedia.org"

def test_with_subdomains():
    host = Host.build(
        subdomains="en",
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    assert str(host.with_subdomains("fr")) == "fr.wikipedia.org"

def test_relative_to_1_host():
    host0 = Host.build(
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    host1 = host0.with_leaf("wikipedia")
    assert str(host0.relative_to(host1)) == "wikipedia.org"
