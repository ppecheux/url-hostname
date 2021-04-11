from collections import namedtuple
from typing import Iterable, Optional, Union

_Domains = namedtuple(
    "Domains", ["subdomains", "second_level_domain", "top_level_domain"]
)


def split_on_dots(domains: Union[Iterable[str], str]):
    if isinstance(domains, str):
        return tuple(domains.split("."))
    splitted_domains = []
    for domain in domains:
        splitted_domains.extend(filter(len, domain.split(".")))
    return tuple(splitted_domains)


class Host:
    """Immutable representation of a host in URL
    Modifying the host will return new instance of the class, thus allowing chaining

    Example:

        >>>  leaf 🍃       domain name
        >>>  _|_              __|__
        >>> ⸍   ⸌            ⸍      ⸌
        >>>  www.prixroberval.utc.fr
        >>> ⸌________________⸍⸌__⸍⸌__⸍
        >>>        |          |    |
        >>> subdomains   second  top
        >>>              domain  domain
        >>>              level   level
    """

    _val: _Domains

    def __new__(
        cls,
        val: str = "",
        *,
        second_level_domain: str = "",
        top_level_domain: str = "",
        subdomains: Optional[Union[Iterable[str], str]] = ()
    ):
        if val and isinstance(val, str):
            raise NotImplementedError
        self = object.__new__(cls)
        if isinstance(val, _Domains):
            self._val = val
            return self

        subdomains = split_on_dots(subdomains)
        domains = _Domains(tuple(subdomains), second_level_domain, top_level_domain)
        self._val = domains
        return self

    def __str__(self) -> str:
        val = self._val
        sub_domains_str = ".".join(val.subdomains)
        if sub_domains_str:
            sub_domains_str += "."
        return sub_domains_str + val.second_level_domain + "." + val.top_level_domain

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, str(self))

    @classmethod
    def build(
        cls,
        second_level_domain: str,
        top_level_domain: str,
        subdomains: Iterable[str] = (),
    ):
        """Creates and returns a new Host:

        Args:
            second_level_domain (str): single part
            top_level_domain (str): level in the hierarchical DNS after the root domain
            subdomains (Iterable[str], optional): parts on the left of the domain name

        Returns:
            Host: new Host instance

        Examples:
            >>> Host.build("utc", "fr")
            Host('utc.fr')
        """
        return cls(
            subdomains=subdomains,
            second_level_domain=second_level_domain,
            top_level_domain=top_level_domain,
        )

    @property
    def domain_name(self):
        """Get the minimal part of the domain space that corresponds to an IP address as a string

        Returns:
            Host: second and top level domains

        Examples:
            >>> host = Host.build("utc", "fr", subdomains=("www", "prixroberval"))
            >>> host.domain_name
            Host('utc.fr')
        """
        return Host.build(
            second_level_domain=self._val[1], top_level_domain=self._val[2]
        )

    @property
    def leaf(self) -> str:
        """Left most part of the domain

        Returns:
            str: host domain's leaf

        Examples:
            >>> host = Host.build("utc", "fr", subdomains=("www", "prixroberval"))
            >>> host.leaf
            'www'
        """
        val = self._val
        return val.subdomains[0] if val.subdomains else val.second_level_domain

    def with_leaf(self, leaf: str):
        """New Host with the left most part of the domain replaced

        Returns:
            Host: new with `leaf` replaced

        Examples:
            >>> host = Host.build("wikipedia", "org", subdomains="en")
            >>> host.with_leaf('fr')
            Host('fr.wikipedia.org')
        """
        assert isinstance(leaf, str)
        val = self._val
        if val.subdomains:
            new_subdomains = val.subdomains[:-1] + (leaf,)
            val = val._replace(subdomains=new_subdomains)
        else:
            val = val._replace(second_level_domain=leaf)
        return Host(val)

    def with_subdomains(self, subdomains: Union[Iterable[str], str]):
        """New Host with `subdomains` replaced

        Args:
            subdomains (Union[Iterable[str], str]): subdomains with leaf at left

        Returns:
            Host: new with `subdomains` replaced

        Examples:
            >>> host = Host.build("utc", "fr", subdomains=("www", "prixroberval"))
            >>> host.with_leaf('prixroberval')
            Host('prixroberval.utc.fr')
        """
        subdomains = split_on_dots(subdomains)
        val = self._val._replace(subdomains=subdomains)
        return Host(val)

    def is_relative_to(self, *other):
        """Whether or not this Host is relative to other

        Returns:
            bool: whether this Host is relative to other

        Examples:
            >>> docs = Host.build('amazon', 'com', ("docs",'aws'))
            >>> macie = docs.with_subdomains(("us-west-2", "redirection", "macie", "aws"))
            >>> macie.is_relative_to(docs)
            True
        """
        top_levels, second_levels = zip(
            *[
                (
                    o._val.top_level_domain,
                    o._val.second_level_domain,
                )
                for o in other
            ]
        )

        val = self._val
        if all(name == val.top_level_domain for name in top_levels) and all(
            name == val.second_level_domain for name in second_levels
        ):
            return True

        return False

    def relative_to(self, *other):
        """Compute new a version of this Host relative to the path represented by other

        Returns:
            Host: new with common domain names

        Raises:
            ValueError: when no relative host exists

        Examples:
            >>> docs = Host.build('amazon', 'com', ("docs",'aws'))
            >>> macie = docs.with_subdomains(("us-west-2", "redirection", "macie", "aws"))
            >>> macie.relative_to(docs)
            Host('aws.amazon.com')
        """

        if not self.is_relative_to(*other):
            raise ValueError("Provided domains are not relative")

        val = self._val

        common_levels = []
        for levels in zip(
            *(reversed(o._val.subdomains) for o in other), reversed(val.subdomains)
        ):
            unique_levels = set(levels)
            if len(unique_levels) != 1:
                break
            common_levels.append(unique_levels.pop())

        return self.with_subdomains(common_levels)
