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

    <style>
        .disclaimer {
            background: #e9f2ff;
            padding: 10px 12px;
            border-left: 4px solid #7ca8e1;
            border-radius: 5px;
            margin: 0 0 6px;
            font-size: 15px;
            line-height: 1.35;
        }
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

.. csv-table:: Canada Hourly Status
   :file: ./_static/can_hly_status.csv
   :header-rows: 1
   :align: center

.. csv-table:: Canada SYNHD Status
   :file: ./_static/can_syndh_status.csv
   :header-rows: 1
   :align: center

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

