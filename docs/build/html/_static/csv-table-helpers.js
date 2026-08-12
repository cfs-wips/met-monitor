// csv-table-helpers.js
// Loads Pyodide and exposes a Python `process_cell(date, column, value, mapping)` function
// to be called when a table cell button is clicked. Mapping is loaded from _static/path_map.json

let pyodide = null;
let pyodideReady = false;
let mapping = null;
let mappingPy = null;
let daganPathsPy = null;
let anikomJsonPy = null;

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
  // load the external Python helper module for per-table functions
  try {
    const resp = await fetch('_static/csv_table_helpers.py');
    if (resp.ok) {
      const pyText = await resp.text();
      await pyodide.runPythonAsync(pyText);
      window.csvTablePyHelperLoaded = true;
      console.log('csv_table_helpers.py loaded in pyodide');
    } else {
      console.warn('Could not fetch csv_table_helpers.py:', resp.status);
    }
  } catch (e) {
    console.warn('Failed to load python helper', e);
  }

  // fetch mapping JSON from static files
  try {
    const resp = await fetch('_static/path_map.json');
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
    const resp = await fetch('_static/dagan_paths.json');
    if (resp.ok) {
      const daganData = await resp.json();
      daganPathsPy = pyodide.toPy(daganData);
      pyodide.globals.set('dagan_paths_json', daganPathsPy);
    }
  } catch (e) {
    console.warn('Failed to load dagan_paths.json', e);
  }

  try {
    const resp = await fetch('_static/Anikom.json');
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

          let pyFunc = null;
          try {
            pyFunc = pyodide.globals.get('process_cell_can_hly');
          } catch (e) {
            try {
              pyFunc = pyodide.globals.get('process_cell');
            } catch (ee) {
              pyFunc = null;
            }
          }

          if (!pyFunc) {
            throw new Error('Python helper function not available');
          }

          const res = pyFunc(dateText, columnName);
          const out = res.toString();
          console.log('Python output', out);
          outputDiv.textContent = out;
          if (navigator.clipboard) await navigator.clipboard.writeText(out).catch(()=>{});
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
