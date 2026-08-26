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

extensions = [
    "sphinx_design",
    "sphinx_copybutton",
    ]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'cloud'
html_static_path = ['_static']

# Show a global table-of-contents in the sidebar so all toctree entries appear
html_sidebars = {
    '**': ['globaltoc.html', 'relations.html', 'searchbox.html']
}

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

# also copy over the .json files from the UTILS directory to the _static directory
utils_dir = project_root / "SCRIPTS" / "UTILS"
if os.path.exists(utils_dir):
    for filename in os.listdir(utils_dir):
        if filename.endswith(".json"):
            shutil.copy(os.path.join(utils_dir, filename), static_dir)


# Note: helper functions are intentionally not registered at build time.
# This project relies on client-side Pyodide to load `csv_table_helpers.py`
# in the browser; the JavaScript loader injects JSON globals and calls
# the Python helpers at runtime. Keep conf.py minimal to avoid build-time
# template dependencies.