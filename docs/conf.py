# -*- coding: utf-8 -*-
"""
docs.conf.py
November 14, 2019
@author Francois Roy
"""
import os
import sys

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, project_root)
sys.path.insert(1, os.path.abspath('./images/'))

# sys.path.insert(0, DOC_DIR) from motor
# sys.path.insert(1, DOC_IMAGE_DIR

# General information about the project.
project = u'fem'
copyright = u'2020, Francois Roy'
author = u'Indigo Francois Roy'
html_logo = 'images/logo.png'
html_favicon = 'images/favicon.png'

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.graphviz',
    'sphinxcontrib.bibtex',
]

numfig = True
numfig_format = {'figure': 'Figure %s',
                 'table': 'Table %s',
                 'code-block': 'Listing %s',
                 'section': 'Section'}
templates_path = ['_templates']
html_static_path = ['_static']

html_show_sourcelink = False
source_suffix = ['.rst']
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db']
pygments_style = 'sphinx'
todo_include_todos = True
html_theme = 'alabaster'
html_theme_options = {'show_powered_by': False,
                      'page_width': '1200px',
                      'fixed_sidebar': True}
# add in each page
rst_prolog = """
.. role:: red
"""
html_sidebars = {
        '**': [
            'navigation.html', 'localtoc.html', 'searchbox.html',
    ]
}
htmlhelp_basename = 'doc'
latex_elements = {
}
