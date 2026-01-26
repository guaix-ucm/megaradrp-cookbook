# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'megara-cookbook'
copyright = '2018-2025, Universidad Complutense de Madrid'
author = 'África Castillo-Morales, Sergio Pascual, Armando Gil de Paz,\nNicolás Cardiel, Mario Chamorro-Cazorla'
# NOTE: see below for author list in LaTeX document

# The full version, including alpha/beta/rc tags
release = '2025.05.16'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
    'sphinx_copybutton',
    'sphinx_new_tab_link',   # external links open in new tab
]
copybutton_prompt_text = "(megara) $ "
copybutton_only_copy_prompt_lines = False
# allow to exclude the copybutton in selected blocks
copybutton_selector = "div:not(.no-copybutton) > div.highlight > pre"


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
#html_logo = 'logo.png'
html_logo = '_static/logo.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
def setup(app):
    app.add_css_file("custom.css")

# This doesn't work. Use html_logo above (NCL, 20241010).
html_theme_options = {
    #'logo': 'logo.png',
    #'show_related': True,
    #'show_relbar_bottom': True,
    #'show_relbar_top': False
}

# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
    'preamble': r'''
\usepackage{graphicx}
\usepackage{transparent}
''',
    'maketitle': r'''
\begin{titlepage}

  \sffamily % Cambia a fuente sans serif
  \bfseries
  \parbox{\textwidth}{%
  \centering

  {\Huge MEGARA}

  {\huge DATA REDUCTION COOKBOOK \par}

  \vspace{1.0 cm}

  {\Large
  \begin{tabular}{c}
  África Castillo-Morales \\
  Sergio Pascual \\
  Armando Gil de Paz \\
  Nicolás Cardiel \\
  Mario Chamorro-Cazorla
  \end{tabular}

  \vspace{1 cm}

  \centerline{%
  \includegraphics[width=0.95\paperwidth,keepaspectratio]{../../cookbook/_static/logo.png}%
  }%end of centerline

  \vspace{0.5 cm}

  {\large Version: 2025.05.16}

  {\large The most up-to-date version of this document is available at}

  \vspace{2 mm}

  {\large \url{https://guaix-ucm.github.io/megaradrp-cookbook/}}}
  }%end of parbox
\end{titlepage}
''',
}

