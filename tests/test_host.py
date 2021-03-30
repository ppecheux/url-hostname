from url_hostname.host import Host
from pytest import fixture


@fixture
def www_prixroberval_utc_fr():
    return Host.build("utc", "fr", subdomains=("www", "prixroberval"))


def test_str():
    host = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert str(host) == "wikipedia.org"


def test_repr():
    host = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert repr(host) == "Host('wikipedia.org')"


def test_subdomains_str(www_prixroberval_utc_fr):
    assert str(www_prixroberval_utc_fr) == "www.prixroberval.utc.fr"


def test_domain_name_prop(www_prixroberval_utc_fr):
    utc_fr = www_prixroberval_utc_fr.domain_name
    assert isinstance(utc_fr, Host)
    assert str(utc_fr) == "utc.fr"


def test_leaf():
    host = Host.build(second_level_domain="wikipedia", top_level_domain="org")
    assert host.leaf == "wikipedia"


def test_subdomains_leaf(www_prixroberval_utc_fr):
    assert www_prixroberval_utc_fr.leaf == "www"


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
