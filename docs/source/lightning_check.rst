.. raw:: html

    <style>
            .disclaimer { background: |text_color|; padding: 10px 12px; border-left: 4px solid black; border-radius: 5px; margin: 0 0 6px; font-size: 15px; line-height: 1.35; }
    </style>

Lightning Feed
^^^^^^^^^^^^^^

Lightning data are pulled from the CLDN feed every 15 minutes. 
However, the timing scripts is only run once per hours. 

Below are the most recent lightning strike times and locations pulled every 15 minutes from the CLDN feed.

.. raw:: html

    </div>

    <div class="disclaimer">
        <strong>Time since last strike in DB: |lightning_time|</strong><br>
    </div>


    <div class="disclaimer">
        <strong>|text|</strong><br>
    </div>

.. csv-table:: Lightning Data (table built at |lightning_time|)
   :file: ./_static/lightning_data.csv
   :header: "Datetime", "Lat", "Lon", "Peak Current", "Multi Flash"
   :widths: 15, 10, 10, 10, 10
   :align: center

.. Now get the time difference between the Datetime column (index 0) and lightning time

