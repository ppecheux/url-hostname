from collections import namedtuple
from typing import Iterable, Optional, Union

_Domains = namedtuple(
    'Domains', ['subdomains', 'second_level_domain', 'top_level_domain'])

def split_on_dots(domains: Union[Iterable[str], str]):
    if isinstance(domains, str):
        return tuple(domains.split('.'))
    splitted_domains = []
    for domain in domains:
        splitted_domains.extend(filter(len,domain.split('.')))
    return tuple(splitted_domains)

class Host:

    _val: _Domains

    def __new__(cls, val: str = "", *,
                second_level_domain: str = "",
                top_level_domain: str = "",
                subdomains: Optional[Union[Iterable[str], str]] = []):
        if val and isinstance(val, str):
            raise NotImplementedError
        self = object.__new__(cls)
        if isinstance(val, _Domains):
            self._val = val
            return self

        subdomains = split_on_dots(subdomains)
        domains = _Domains(tuple(subdomains),
                           second_level_domain, top_level_domain)
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
    def build(cls,
              second_level_domain: str,
              top_level_domain: str,
              subdomains: Optional[Iterable[str]] = []
              ):
        return cls(subdomains=subdomains,
                   second_level_domain=second_level_domain,
                   top_level_domain=top_level_domain)

    @property
    def domain_name(self):
        return '.'.join(self._val[1:])

    @property
    def leaf(self) -> str:
        val = self._val
        return val.subdomains and val.subdomains[0] or val.second_level_domain

    def with_leaf(self, leaf: str):
        assert isinstance(leaf, str)
        val = self._val
        if val.subdomains:
            new_subdomains = val.subdomains[:-1]+(leaf,)
            val = val._replace(subdomains=new_subdomains)
        else:
            val = val._replace(second_level_domain=leaf)
        return Host(val)

    def with_subdomains(self, subdomains: Union[Iterable[str], str]):
        subdomains = split_on_dots(subdomains)
        val = self._val._replace(subdomains=subdomains)
        return Host(val)

    def relative_to(self, *other):
        tlds, slds, sds = zip(*[
            (o._val.top_level_domain,
             o._val.second_level_domain,
             o._val.subdomains)
            for o in other
        ])

        val = self._val
        if not all(name == val.top_level_domain for name in tlds):
            if len(tlds) == 1:
                raise ValueError(
                    "{} is not relative to {}".format(
                        val.top_level_domain, tlds[0])
                )
            else:
                raise ValueError(
                    "one of the top level domain is different"
                )

        if not all(name == val.second_level_domain for name in slds):
            if len(slds) == 1:
                raise ValueError(
                    "{} is not relative to {}".format(
                        val.top_level_domain, slds[0])
                )
            else:
                raise ValueError(
                    "one of the top second level domain is different"
                )

        i, max_i = 0, max(map(len,sds))
        while i<max_i and all(sd[i]==val.subdomains[i] for sd in sds):
            i+=1

        return self.with_subdomains(val.subdomains[:i])
