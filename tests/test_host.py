from pytest import fixture
from url_hostname.host import Host


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


def test_with_subdomains_2(www_prixroberval_utc_fr: Host):
    assert (
        str(www_prixroberval_utc_fr.with_subdomains("prixroberval"))
        == "prixroberval.utc.fr"
    )


def test_with_subdomains_tuple():
    host = Host.build(second_level_domain="utc", top_level_domain="fr")
    assert (
        str(host.with_subdomains(("www", "prixroberval"))) == "www.prixroberval.utc.fr"
    )


def test_is_relative_to_1_host():
    host0 = Host.build(
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    host1 = host0.with_leaf("wikipedia")
    assert host0.is_relative_to(host1)


def test_is_not_relative_to_1_host():
    host0 = Host.build(
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    host1 = host0.with_leaf("utc")
    assert not host0.is_relative_to(host1)


def test_is_not_relative_to_n_host():
    host0 = Host.build(
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    hosts = [host0.with_leaf("utc") for _ in range(3)]
    assert not host0.is_relative_to(*hosts)


def test_is_relative_to_n_host():
    host0 = Host.build(
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    hosts = [host0.with_leaf("wikipedia") for _ in range(3)]
    assert host0.is_relative_to(*hosts)


def test_relative_to_1_host():
    host0 = Host.build(
        second_level_domain="wikipedia",
        top_level_domain="org",
    )
    host1 = host0.with_leaf("wikipedia")
    assert str(host0.relative_to(host1)) == "wikipedia.org"


def test_relative_to_sub_domains():
    host0 = Host.build(
        subdomains=("us-west-2", "redirection", "macie", "aws"),
        second_level_domain="amazon",
        top_level_domain="com",
    )
    host1 = host0.domain_name.with_subdomains(("docs", "aws"))
    assert str(host0) == "us-west-2.redirection.macie.aws.amazon.com"
    assert str(host1) == "docs.aws.amazon.com"
    host_rel = host0.relative_to(host1)
    assert str(host_rel) == "aws.amazon.com"


def test_relative_to_sub_domains_big():
    docs = Host.build("amazon", "com", ("docs", "aws"))
    macie = docs.with_subdomains(("us-west-2", "redirection", "macie", "aws"))

    assert str(macie) == "us-west-2.redirection.macie.aws.amazon.com"
    assert str(docs) == "docs.aws.amazon.com"
    host_rel = macie.relative_to(docs)
    assert str(host_rel) == "aws.amazon.com"
