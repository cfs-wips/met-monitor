# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'met-monitor'
copyright = '2026, BuchartL'
author = 'BuchartL'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'cloud'
html_static_path = ['_static']

# move files to static as needed
import os
import shutil
from datetime import datetime
from pathlib import Path

# get path to the _static directory
static_dir = os.path.join(os.path.dirname(__file__), '_static')
# path to the temp directory
project_root = Path(__file__).resolve().parent.parent.parent
temp_dir = project_root / "SCRIPTS" / "temp"
print(f"Temp directory: {temp_dir}")

# add a timestamp substitution for the Lightning Data title
lightning_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
rst_epilog = f"""
.. |lightning_time| replace:: {lightning_time}
"""

# move all files from temp to static
if os.path.exists(temp_dir):
    for filename in os.listdir(temp_dir):
        shutil.copy(os.path.join(temp_dir, filename), static_dir)
