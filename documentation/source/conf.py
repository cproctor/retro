# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Retro Games'
copyright = '2024, Chris Proctor'
author = 'Chris Proctor'
release = '1.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

intersphinx_mapping = {
    'quest': ('https://questgame.readthedocs.io/en/latest/', None),
    'arcade': ('https://api.arcade.academy/en/latest/', None),
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
