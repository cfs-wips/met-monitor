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

    # Fallback: try to load a local file relative to this source file, but be forgiving
    try:
        path = Path(__file__).resolve().with_name(filename)
        if path.exists():
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        # In Pyodide/browser contexts __file__ may not be defined or filesystem unavailable.
        pass

    # Final fallback: return an empty mapping so callers don't crash at runtime.
    return {}


def process_cell(table, date, column):
    """Build a path string from mapping templates and the clicked values.

    mapping is expected to be a dict with a 'templates' dict containing named templates.
    Example template: '{base}/{date}/{column}/{value}.txt'
    """
    path_mapping = _load_json('dagan_paths.json')

    base_path = path_mapping.get('bulletins')  

    if table == "can_hly":

        can_dirs = path_mapping.get('can_dirs') or []
        first_dirs = can_dirs if len(can_dirs) > 0 else None
        sub_dir = path_mapping.get('can_subdir')

    elif table == "usa_hly":

        usa_dirs = path_mapping.get('usa_dirs') or []
        first_dirs = usa_dirs if len(usa_dirs) > 0 else None
        sub_dir = path_mapping.get('usa_subdir')

    elif table == "mex_hly":
        mex_dirs = path_mapping.get('mex_dirs') or []
        first_dirs = mex_dirs if isinstance(mex_dirs, list) and len(mex_dirs) > 0 else mex_dirs
        sub_dir = path_mapping.get('mex_subdir')

    elif table == "eurasn_hly":
        eurasn_dirs = path_mapping.get('eurasn_dirs') or []
        first_dirs = eurasn_dirs if isinstance(eurasn_dirs, list) and len(eurasn_dirs) > 0 else eurasn_dirs
        sub_dir = path_mapping.get('eurasn_subdir')

    elif table == "can_syno":
        dir = path_mapping.get('can_dirs') or []

    listed_dirs = []
    # create a list of of paths if there more than one first directory, otherwise just return a single path
    if table == "can_hly" or table == "usa_hly":
        # now call Anikom parser here for cleaner python functions
        fname = anikom_parser(date, column)

        if isinstance(first_dirs, list):
            for first_dir in first_dirs:
                if first_dir:
                    listed_dirs.append(f"{base_path}{first_dir}/{sub_dir}/{fname}")
        elif first_dirs:
            listed_dirs.append(f"{base_path}{first_dirs}/{sub_dir}/{fname}")

    elif table == "mex_hly" or table == "eurasn_hly":
        # mex_dirs may be a string or a list; build a human-friendly instruction
        if isinstance(first_dirs, list):
            for fd in first_dirs:
                listed_dirs.append(f"Go run {fd}/{sub_dir}")
        elif first_dirs:
            listed_dirs.append(f"Go run {first_dirs}/{sub_dir} {date}{column} {date}{column} --rr")

    elif table == "can_syno":
        listed_dirs = dir + "/rerun the synoptic data for this hour if you please.."

    else:
        print("error no table specified...")

    return listed_dirs


def process_cell_can_hly(date, column):
    """Table-specific entry point for Canada Hourly Status."""
    # In browser mode these JSON objects are injected by the JavaScript loader.
    _load_json('dagan_paths.json')

    res = process_cell(table='can_hly', date=date, column=column)
    if isinstance(res, (list, tuple)):
        return '\n'.join(str(x) for x in res)
    return str(res)


def process_cell_usa_hly(date, column):
    """Table-specific entry point for USA Hourly Status."""
    # In browser mode these JSON objects are injected by the JavaScript loader.
    _load_json('dagan_paths.json')

    res = process_cell(table='usa_hly', date=date, column=column)
    if isinstance(res, (list, tuple)):
        return '\n'.join(str(x) for x in res)
    return str(res)


def process_cell_mex_hly(date, column):
    """Table-specific entry point for Mexico Hourly Status."""
    # In browser mode these JSON objects are injected by the JavaScript loader.
    _load_json('dagan_paths.json')

    res = process_cell(table='mex_hly', date=date, column=column)
    if isinstance(res, (list, tuple)):
        return '\n'.join(str(x) for x in res)
    return str(res)


def process_cell_eurasn_hly(date, column):
    """Table-specific entry point for Eurasian Hourly Status."""
    # In browser mode these JSON objects are injected by the JavaScript loader.
    _load_json('dagan_paths.json')

    res = process_cell(table='eurasn_hly', date=date, column=column)
    if isinstance(res, (list, tuple)):
        return '\n'.join(str(x) for x in res)
    return str(res)    


def process_cell_syno(date, column):
    _load_json('dagan_paths.json')
    
    res = process_cell(table='can_syno', date=date, column=column)
    if isinstance(res, (list, tuple)):
        return '\n'.join(str(x) for x in res)
    return str(res)


def anikom_parser(date, column):
    "Get the Anikom file name for the date and column"
    anikom_mapping = _load_json('Anikom.json')

    mday = date[6:8]  # extract the day from the date string
    anikom_day = anikom_mapping["date"][mday]

    anikom_hour = anikom_mapping["hour"][str(column)]

    file_name = f"{anikom_day}{anikom_hour}00__{anikom_hour}0.000"
    return file_name