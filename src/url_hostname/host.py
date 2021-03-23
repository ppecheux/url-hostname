from collections import namedtuple
from typing import Iterable, Optional

_Domains = namedtuple('Domains',['subdomains', 'second_level_domain', 'top_level_domain'])

class Host:

    _val: _Domains

    def __new__(cls, val: str = "", *,
                second_level_domain: str,
                top_level_domain: str,
                subdomains: Optional[Iterable[str]] = []):
        if isinstance(val, str):
            raise NotImplementedError
        self = object.__new__(cls)
        if isinstance(val, _Domains):
            self._val = val
            return self
        domains = _Domains(tuple(subdomains), second_level_domain, top_level_domain)
        self._val = domains
        return self

    def __str__(self):
        val = self._val
        return ".".join(reversed(val._subdomains)) + "." + val._second_level_domain + "." + val._top_level_domain

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
    def leaf(self):
        val = self._val
        return val.subdomains[-1] or val.second_level_domain


    def with_leaf(self, leaf:str):
        assert isinstance(leaf, str)
        val = self._val
        if val.subdomains:
            val._replace(subdomains=val.subdomains[:-1]+leaf)
        else:
            val._replace(second_level_domain=leaf)
        return Host(val)
