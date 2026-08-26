// csv-table-helpers.js
// Loads Pyodide and exposes a Python `process_cell(date, column, value, mapping)` function
// to be called when a table cell button is clicked. Mapping is loaded from _static/path_map.json

let pyodide = null;
let pyodideReady = false;
let mapping = null;
let mappingPy = null;
let daganPathsPy = null;
let anikomJsonPy = null;

// Compute a robust `_static/` base URL from the script's `src` so fetches
// work when the site is served under a subpath (GitHub Pages) or from
// a local HTTP server. We resolve relative to the script tag and
// prefer the enclosing `_static/` directory.
function computeCsvStaticBase() {
  const script = document.currentScript || document.scripts[document.scripts.length - 1];
  const src = script && script.src ? script.src : window.location.href;
  try {
    // `new URL('.', src)` gives the directory containing the script and
    // always ends with '/'. If the script is already in `_static/`, this
    // will be the exact folder we need. If not, fall back to appending
    // `_static/` to that directory.
    const dir = new URL('.', src).toString();
    if (dir.endsWith('_static/')) return dir;
    return new URL('_static/', dir).toString();
  } catch (e) {
    // Best-effort fallback to a relative static path
    return './_static/';
  }
}

let _csvStaticBase = null;

async function loadPyodideAndMapping() {
  if (pyodideReady) return;
  // load pyodide runtime script
  if (!window.loadPyodide) {
    await new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js';
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/' });
  window.csvTablePyHelperLoaded = false;
  // ensure we have a static base computed
  try {
    if (!_csvStaticBase) _csvStaticBase = computeCsvStaticBase();
  } catch (e) {
    _csvStaticBase = './_static/';
  }

  // load the external Python helper module for per-table functions
  try {
    const helperUrl = new URL('csv_table_helpers.py', _csvStaticBase).toString();
    const resp = await fetch(helperUrl);
    if (resp.ok) {
      const pyText = await resp.text();
      await pyodide.runPythonAsync(pyText);
      window.csvTablePyHelperLoaded = true;
      console.log('csv_table_helpers.py loaded in pyodide (from)', helperUrl);
        // Diagnostic: list expected helper names and whether they exist
        try {
          const names = ['process_cell', 'process_cell_can_hly', 'process_cell_usa_hly', 'process_cell_mex_hly', 'process_cell_eurasn_hly'];
          const present = {};
          for (const n of names) {
            try {
              present[n] = !!pyodide.globals.get(n);
            } catch (e) {
              present[n] = false;
            }
          }
          console.log('Python helper availability:', present);
        } catch (diagErr) {
          console.warn('Diagnostic check failed', diagErr);
        }
    } else {
      console.warn('Could not fetch csv_table_helpers.py:', resp.status);
    }
  } catch (e) {
    console.warn('Failed to load python helper', e);
  }

  // fetch mapping JSON from static files
  try {
    const mappingUrl = new URL('path_map.json', _csvStaticBase).toString();
    const resp = await fetch(mappingUrl);
    if (resp.ok) {
      mapping = await resp.json();
      mappingPy = pyodide.toPy(mapping);
      pyodide.globals.set('mapping_json', mappingPy);
    } else {
      mapping = {};
      mappingPy = pyodide.toPy(mapping);
      pyodide.globals.set('mapping_json', mappingPy);
    }
  } catch (e) {
    mapping = {};
    mappingPy = pyodide.toPy(mapping);
    pyodide.globals.set('mapping_json', mappingPy);
  }

  try {
    const daganUrl = new URL('dagan_paths.json', _csvStaticBase).toString();
    const resp = await fetch(daganUrl);
    if (resp.ok) {
      const daganData = await resp.json();
      daganPathsPy = pyodide.toPy(daganData);
      pyodide.globals.set('dagan_paths_json', daganPathsPy);
    }
  } catch (e) {
    console.warn('Failed to load dagan_paths.json', e);
  }

  try {
    const anikomUrl = new URL('Anikom.json', _csvStaticBase).toString();
    const resp = await fetch(anikomUrl);
    if (resp.ok) {
      const anikomData = await resp.json();
      anikomJsonPy = pyodide.toPy(anikomData);
      pyodide.globals.set('anikom_json', anikomJsonPy);
    }
  } catch (e) {
    console.warn('Failed to load Anikom.json', e);
  }

  pyodideReady = true;
}

function csvCellClassCanadaHourly(value) {
  if (!value) return 'csv-cell-neutral';
  if (/^XX$/i.test(value)) return 'csv-cell-error';
  var num = parseInt(value, 10);
  if (isNaN(num)) return 'csv-cell-neutral';
  if (num >= 80) return 'csv-cell-success';
  if (num >= 77 && num <= 79) return 'csv-cell-warning';
  return 'csv-cell-error';
}

function csvCellClassUSAHourly(value) {
  if (!value) return 'csv-cell-neutral';
  if (/^XX$/i.test(value)) return 'csv-cell-error';
  var num = parseInt(value, 10);
  if (isNaN(num)) return 'csv-cell-neutral';
  if (num >= 80) return 'csv-cell-success';
  return 'csv-cell-error';
}

function csvCellClassMexHourly(value) {
  if (!value) return 'csv-cell-neutral';
  if (/^XX$/i.test(value)) return 'csv-cell-error';
  var num = parseInt(value, 10);
  if (isNaN(num)) return 'csv-cell-neutral';
  if (num >= 0) return 'csv-cell-success';
  return 'csv-cell-error';
}

function csvCellClassEurasnHourly(value) {
  if (!value) return 'csv-cell-neutral';
  if (/^XX$/i.test(value)) return 'csv-cell-error';
  var num = parseInt(value, 10);
  if (isNaN(num)) return 'csv-cell-neutral';
  if (num >= 0) return 'csv-cell-success';
  return 'csv-cell-error';
}

function ensureOutputBelowTable(wrapper, table) {
  let outputDiv = wrapper.querySelector('.csv-table-output');
  if (!outputDiv) {
    outputDiv = document.createElement('div');
    outputDiv.className = 'csv-table-output';
    outputDiv.style.marginTop = '0.75rem';
    outputDiv.style.padding = '0.5rem 0.75rem';
    outputDiv.style.border = '1px solid #d0d7de';
    outputDiv.style.borderRadius = '6px';
    outputDiv.style.background = '#f6f8fa';
    outputDiv.style.fontFamily = 'monospace';
    outputDiv.style.whiteSpace = 'pre-wrap';
    outputDiv.style.wordBreak = 'break-word';
    table.insertAdjacentElement('afterend', outputDiv);
  }
  return outputDiv;
}

function ensureCopyButton(outputDiv) {
  let btn = outputDiv.querySelector('.csv-copy-btn');
  if (!btn) {
    btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'csv-copy-btn copybtn';
    btn.textContent = 'Copy';
    btn.title = 'Copy path to clipboard';
    btn.style.marginLeft = '0.5rem';
    btn.style.display = 'inline-block';
    btn.addEventListener('click', async function() {
      const text = outputDiv.textContent || '';
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(text);
        } else {
          const ta = document.createElement('textarea');
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          ta.remove();
        }
      } catch (e) {
        console.warn('Copy failed', e);
      }
    });
    outputDiv.appendChild(btn);
  }
  return btn;
}

async function makeCsvCellsClickable(wrapperSelector, cellClassFn) {
  // start loading pyodide in background
  loadPyodideAndMapping().catch(console.error);

  const wrapper = document.querySelector(wrapperSelector);
  if (!wrapper) return;

  const table = wrapper.querySelector('table');
  if (!table) return;

  const outputDiv = ensureOutputBelowTable(wrapper, table);

  // compute headers
  const headers = Array.from(table.querySelectorAll('thead th')).map(h => h.textContent.trim());

  table.querySelectorAll('tbody tr').forEach(function(row) {
    // find date cell value (assume first td is date)
    const dateCell = row.querySelector('td');
    const dateText = dateCell ? dateCell.textContent.trim() : '';

    row.querySelectorAll('td').forEach(function(td, colIndex) {
      const value = td.textContent.trim();
      // main value button (copies the raw cell value)
      const valueBtn = document.createElement('button');
      valueBtn.type = 'button';
      valueBtn.textContent = value;
      valueBtn.className = cellClassFn(value);

      valueBtn.addEventListener('click', async function() {
        // on click, run python helper (if available) to build a path, show it below the table, and copy it
        const columnName = headers[colIndex] || String(colIndex);

        // show a quick loading state
        const prevText = valueBtn.textContent;
        valueBtn.textContent = 'Processing...';

        try {
          await loadPyodideAndMapping();
          if (!pyodideReady || !pyodide) {
            throw new Error('Pyodide did not initialize');
          }

          // choose preferred python helper based on which cell-class function was passed
          const preferredPyNames = [];
          try {
            if (cellClassFn === window.csvCellClassUSAHourly) preferredPyNames.push('process_cell_usa_hly');
          } catch (e) {}
          try {
            if (cellClassFn === window.csvCellClassMexHourly) preferredPyNames.push('process_cell_mex_hly');
          } catch (e) {}
          try {
            if (cellClassFn === window.csvCellClassEurasnHourly) preferredPyNames.push('process_cell_eurasn_hly');
          } catch (e) {}
          try {
            if (cellClassFn === window.csvCellClassCanadaHourly) preferredPyNames.push('process_cell_can_hly');
          } catch (e) {}
          preferredPyNames.push('process_cell');

          let pyFunc = null;
          for (const name of preferredPyNames) {
            try {
              pyFunc = pyodide.globals.get(name);
              if (pyFunc) break;
            } catch (e) {
              // not available, try next
            }
          }

          if (!pyFunc) {
            throw new Error('Python helper function not available');
          }

          const res = pyFunc(dateText, columnName);
          const out = res.toString();
          console.log('Python output', out);
          outputDiv.textContent = out;
          // Do not auto-copy. Provide a copy button instead.
          ensureCopyButton(outputDiv);
          res.destroy && res.destroy();
        } catch (err) {
          console.error('Cell processing failed', err);
          outputDiv.textContent = 'Error: ' + (err.message || 'processing failed');
        } finally {
          valueBtn.textContent = prevText;
        }
      });

      td.textContent = '';
      td.appendChild(valueBtn);
    });
  });
}

// export for inline usage
window.makeCsvCellsClickable = makeCsvCellsClickable;
window.csvCellClassCanadaHourly = csvCellClassCanadaHourly;
window.csvCellClassUSAHourly = csvCellClassUSAHourly;
window.csvCellClassMexHourly = csvCellClassMexHourly;
window.csvCellClassEurasnHourly = csvCellClassEurasnHourly;
