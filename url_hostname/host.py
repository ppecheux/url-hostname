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
    """Immutable representation of a host in URL"""

    _val: _Domains

    def __new__(
        cls,
        val: str = "",
        *,
        second_level_domain: str = "",
        top_level_domain: str = "",
        subdomains: Optional[Union[Iterable[str], str]] = []
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
        subdomains: Optional[Iterable[str]] = tuple(),
    ):
        return cls(
            subdomains=subdomains,
            second_level_domain=second_level_domain,
            top_level_domain=top_level_domain,
        )

    @property
    def domain_name(self):
        """get the minimal part of the domain space that corresponds to an IP address as a string

        Returns:
            Host: second and top level domains

        Examples:
            >>> Host.build("utc", "fr", subdomains=("www", "prixroberval"))
            >>> utc_fr = host.domain_name
            >>> isinstance(utc_fr, Host)
            True
            >>> str(utc_fr)
            "utc.fr"
        """
        return Host.build(second_level_domain=self._val[1], top_level_domain=self._val[2])

    @property
    def leaf(self) -> str:
        val = self._val
        return val.subdomains[0] if val.subdomains else val.second_level_domain

    def with_leaf(self, leaf: str):
        assert isinstance(leaf, str)
        val = self._val
        if val.subdomains:
            new_subdomains = val.subdomains[:-1] + (leaf,)
            val = val._replace(subdomains=new_subdomains)
        else:
            val = val._replace(second_level_domain=leaf)
        return Host(val)

    def with_subdomains(self, subdomains: Union[Iterable[str], str]):
        subdomains = split_on_dots(subdomains)
        val = self._val._replace(subdomains=subdomains)
        return Host(val)

    def relative_to(self, *other):
        top_levels, second_levels, subs = zip(
            *[
                (o._val.top_level_domain, o._val.second_level_domain, o._val.subdomains)
                for o in other
            ]
        )

        val = self._val
        if not all(name == val.top_level_domain for name in top_levels):
            if len(top_levels) == 1:
                raise ValueError(
                    "{} is not relative to {}".format(
                        val.top_level_domain, top_levels[0]
                    )
                )
            raise ValueError("one of the top level domain is different")

        if not all(name == val.second_level_domain for name in second_levels):
            if len(second_levels) == 1:
                raise ValueError(
                    "{} is not relative to {}".format(
                        val.top_level_domain, second_levels[0]
                    )
                )
            raise ValueError("one of the top second level domain is different")

        i, max_i = 0, max(map(len, subs))
        while i < max_i and all(sd[i] == val.subdomains[i] for sd in subs):
            i += 1

        return self.with_subdomains(val.subdomains[:i])
