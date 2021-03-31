# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os #pylint: disable=no-absolute-import
import sys
import pathlib
import re

_project_path = pathlib.Path(__file__).parent.parent.parent
_version_path = _project_path / "url_hostname/__version__.py"


with _version_path.open() as fp:
    try:
        _version_info = re.search(
            r"^__version__ = \""
            r"(?P<major>\d+)"
            r"\.(?P<minor>\d+)"
            r"\.(?P<patch>\d+)"
            r"(?P<tag>.*)?\"$",
            fp.read(),
            re.M,
        ).groupdict()
    except IndexError as version_not_found:
        raise RuntimeError("Unable to determine version.") from version_not_found
sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "url-hostname" #pylint: disable=invalid-name
copyright = "2021, Pierre-Louis Pécheux" # pylint: disable=redefined-builtin, invalid-name, line-too-long
author = "Pierre-Louis Pécheux" #pylint: disable=invalid-name

# The short X.Y version.
version = '{major}.{minor}'.format(**_version_info) #pylint: disable=invalid-name
# The full version, including alpha/beta/rc tags.
release = '{major}.{minor}.{patch}-{tag}'.format(**_version_info) #pylint: disable=invalid-name


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.coverage", "sphinx.ext.napoleon"]

try:
    import sphinxcontrib.spelling  # noqa
    extensions.append('sphinxcontrib.spelling')
except ImportError:
    pass

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "y" #pylint: disable=invalid-name

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster" #pylint: disable=invalid-name

html_theme_options = {
    'logo': 'hotel.png',
    #'description': '',
    'github_user': 'ppecheux',
    'github_repo': 'url-hostname',
    'github_button': True,
    'github_type': 'star',
    'github_banner': True,
    'codecov_button': True,
    'sidebar_collapse': False,
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
