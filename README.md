# met-monitor
A simple sphinx page to monitor the CWFIS weather feed

There are functions in place to generate paths to relevant METAR files depending on the hour of data that is having issues. There are based on pre-existing folder structures and the Anikom format used to name daily and hourly files. 
Additionally, we monitor the CLDN lightning strike feed into the CWFIF. Other upgrades may come come for certain weather or FWI feeds. 

# notes on directory structure and files
UTILS/ sits in the SCRIPTS dir. UTILS contains required paths to access the status files for all weather processing.
temp/ sits in the scripts dir and contains all of the output from the status files as well as the lightning feed that are here. 
      These files are read to the webpage. There simple display of the most recent lightning strike downloads (including time of download)
      The status files are more complex. Each hour's download status will actually be a button - this button returns the path to the temp
      files of the problem data.

Liam.Buchart@NRcan-RNcan.gc.ca
August 4, 2026
