.. met-monitor documentation master file, created by
   sphinx-quickstart on Fri Aug  7 11:57:23 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Weather Stream Monitoring
=========================

Status Files
^^^^^^^^^^^^

7 days worth of status files for the Canadian, US, Mexico, and Eurasian feeds. Additionally, upper air station data. 
Percentages are color coded to indicate the status. 

.. raw:: html

    <div class="csv-table-responsive can-hly-status-wrapper">

.. csv-table:: Canada Hourly Status - can_hly_status.csv
   :file: ./_static/can_hly_status.csv
   :header-rows: 1
   :align: center

.. raw:: html

    </div>

.. raw:: html

    <div class="csv-table-responsive">

.. csv-table:: Canada SYNHD Status - can_syndh_status.csv
   :file: ./_static/can_syndh_status.csv
   :header-rows: 1
   :align: center

.. raw:: html

    </div>

.. raw:: html

    <script src="_static/csv-table-helpers.js"></script>
    <script>
      document.addEventListener('DOMContentLoaded', function() {
        makeCsvCellsClickable('.can-hly-status-wrapper', csvCellClassCanadaHourly);
      });
    </script>

.. raw:: html

    <style>
        .csv-table-responsive { width:100%; overflow-x:auto; margin-bottom:1rem; }
        .csv-table-responsive table { width:100%; border-collapse:collapse; }
        .csv-table-responsive th, .csv-table-responsive td { padding:0.35rem 0.6rem; }
        .csv-table-responsive td button {
            display:inline-block;
            padding:0.35rem 0.5rem;
            border:1px solid rgba(0,0,0,0.06);
            border-radius:4px;
            background:#fff;
            color:inherit;
            text-align:left;
            cursor:pointer;
            vertical-align:middle;
        }
        .csv-table-responsive td .csv-copy-btn {
            margin-left:6px;
            padding:0.2rem 0.45rem;
            font-size:0.85rem;
            border-radius:4px;
            background:#f1f5f9;
            color:#0f172a;
        }
        .csv-table-responsive td button.csv-cell-success { background:#d4edda; color:#155724; }
        .csv-table-responsive td button.csv-cell-warning { background:#fff3cd; color:#856404; }
        .csv-table-responsive td button.csv-cell-error { background:#f8d7da; color:#721c24; }
        .csv-table-responsive td button.csv-cell-neutral { background:#e2e3e5; color:#383d41; }

        .csv-path-output { display:block; margin-top:6px; font-family: monospace; font-size:0.85rem; color:#0f172a; word-break:break-all; }

        .disclaimer { background: #e9f2ff; padding: 10px 12px; border-left: 4px solid #7ca8e1; border-radius: 5px; margin: 0 0 6px; font-size: 15px; line-height: 1.35; }
    </style>

    <div class="disclaimer">
        <strong>Red - Requires re-run: <80% for Canada and USA hourlies. XX for Mexico and Eurasia.</strong><br>
    </div>

    <div class="disclaimer">
         <strong>Yellow - Only used for Canada: near 80% indicating Alberta Agriculture stations likely need to be re-run.</strong><br>
    </div>

    <div class="disclaimer">
          <strong>Green - Running well: >80% for Canada and USA hourlies. Any percentage for Mexico and Eurasia.</strong><br>
    </div>

Lightning Feed
^^^^^^^^^^^^^^

Below are the most recent lightning strike times and locations pulled every 15 minutes from the CLDN feed.

.. csv-table:: Lightning Data (built at |lightning_time|)
   :file: ./_static/lightning_data.csv
   :header: "Datetime", "Lat", "Lon", "Peak Current", "Multi Flash"
   :widths: 15, 10, 10, 10, 10
   :align: center

Scribe
^^^^^^

Environment and Climate Change Canada Scribe data. 

NAEFS
^^^^^

North American Ensemble Forecast System data.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

