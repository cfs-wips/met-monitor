# Python helper for CSV table cell processing
# Edit this file to add per-table functions.

import json
from pathlib import Path


def _load_json(filename):
    """Return JSON from injected Pyodide globals when available or from a local file.

    In browser mode, the JavaScript loader sets the JSON payloads directly into Python
    globals before calling this helper. Relative file paths do not exist there.
    """
    aliases = {
        'dagan_paths.json': 'dagan_paths_json',
        'Anikom.json': 'anikom_json',
    }
    global_name = aliases.get(filename, filename.replace('.json', '_json').replace('-', '_'))
    if global_name in globals():
        return globals()[global_name]

    path = Path(__file__).resolve().with_name(filename)
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)

    raise FileNotFoundError(
        f"Could not find {filename}. In browser mode, it must be loaded with fetch() and exposed as a Python global."
    )


def process_cell(table='can_hly'):
    """Build a path string from mapping templates and the clicked values.

    mapping is expected to be a dict with a 'templates' dict containing named templates.
    Example template: '{base}/{date}/{column}/{value}.txt'
    """
    templates = {}
    path_mapping = _load_json('dagan_paths.json')

    base_path = path_mapping.get('bulletins')  

    if table == "can_hly":
        first_dir = path_mapping.get('can_dir')
        sub_dir = path_mapping.get('can_subdir')

    path = f"{base_path}{first_dir}/{sub_dir}/"

    return path


def process_cell_can_hly(date, column, value, mapping):
    """Table-specific entry point for Canada Hourly Status."""
    # In browser mode these JSON objects are injected by the JavaScript loader.
    _load_json('dagan_paths.json')

    fname = anikom_parser(date, column)
    fstr = process_cell(table='can_hly')

    return f"{fstr}{fname}"


def anikom_parser(date, column):
    "Get the Anikom file name for the date and column"
    anikom_mapping = _load_json('Anikom.json')

    mday = date[6:8]  # extract the day from the date string
    anikom_day = anikom_mapping["date"][mday]

    anikom_hour = anikom_mapping["hour"][str(column)]

    file_name = f"{anikom_day}{anikom_hour}00__{anikom_hour}0.000"
    return file_name