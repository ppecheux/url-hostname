# url-hostname



![image](https://readthedocs.org/projects/url-hostname/badge/?version=latest)

<!-- :target: https://url-hostname.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status -->


![image](https://codecov.io/gh/ppecheux/url-hostname/branch/main/graph/badge.svg)

<!-- :target: https://codecov.io/gh/ppecheux/url-hostname -->

### class url_hostname.host.Host(val: str = '', \*, second_level_domain: str = '', top_level_domain: str = '', subdomains: Union[Iterable[str], str] = ())
Immutable representation of a host in URL
Modifying the host will return new instance of the class, thus allowing chaining

### Example

```python
>>>  leaf 🍃       domain name
>>>  _|_              __|__
>>> ⸍   ⸌            ⸍      ⸌
>>>  www.prixroberval.utc.fr
>>> ⸌________________⸍⸌__⸍⸌__⸍
>>>        |          |    |
>>> subdomains   second  top
>>>              domain  domain
>>>              level   level
```


#### classmethod build(second_level_domain: str, top_level_domain: str, subdomains: Iterable[str] = ())
Creates and returns a new Host:


* **Parameters**

    
    * **second_level_domain** (*str*) -- single part


    * **top_level_domain** (*str*) -- level in the hierarchical DNS after the root domain


    * **subdomains** (*Iterable**[**str**]**, **optional*) -- parts on the left of the domain name



* **Returns**

    new Host instance



* **Return type**

    Host


### Examples

```python
>>> Host.build("utc", "fr")
Host('utc.fr')
```


#### property domain_name()
Get the minimal part of the domain space that corresponds to an IP address as a string


* **Returns**

    second and top level domains



* **Return type**

    Host


### Examples

```python
>>> host = Host.build("utc", "fr", subdomains=("www", "prixroberval"))
>>> host.domain_name
Host('utc.fr')
```


#### is_relative_to(\*other)
Whether or not this Host is relative to other


* **Returns**

    whether this Host is relative to other



* **Return type**

    bool


### Examples

```python
>>> docs = Host.build('amazon', 'com', ("docs",'aws'))
>>> macie = docs.with_subdomains(("us-west-2", "redirection", "macie", "aws"))
>>> macie.is_relative_to(docs)
True
```


#### property leaf()
Left most part of the domain


* **Returns**

    host domain's leaf



* **Return type**

    str


### Examples

```python
>>> host = Host.build("utc", "fr", subdomains=("www", "prixroberval"))
>>> host.leaf
'www'
```


#### relative_to(\*other)
Compute new a version of this Host relative to the path represented by other


* **Returns**

    new with common domain names



* **Return type**

    Host



* **Raises**

    **ValueError** -- when no relative host exists


### Examples

```python
>>> docs = Host.build('amazon', 'com', ("docs",'aws'))
>>> macie = docs.with_subdomains(("us-west-2", "redirection", "macie", "aws"))
>>> macie.relative_to(docs)
Host('aws.amazon.com')
```


#### with_leaf(leaf: str)
New Host with the left most part of the domain replaced


* **Returns**

    new with leaf replaced



* **Return type**

    Host


### Examples

```python
>>> host = Host.build("wikipedia", "org", subdomains="en")
>>> host.with_leaf('fr')
Host('fr.wikipedia.org')
```


#### with_subdomains(subdomains: Union[Iterable[str], str])
New Host with subdomains replaced


* **Parameters**

    **subdomains** (*Union**[**Iterable**[**str**]**, **str**]*) -- subdomains with leaf at left



* **Returns**

    new with subdomains replaced



* **Return type**

    Host


### Examples

```python
>>> host = Host.build("utc", "fr", subdomains=("www", "prixroberval"))
>>> host.with_leaf('prixroberval')
Host('prixroberval.utc.fr')
```

<!-- toctree::.. image:: https://readthedocs.org/projects/ur/badge/?version=latest

:maxdepth: 2
:caption: Contents: -->
# Indices and tables


* Index


* Module Index


* Search Page
