""" 

    Grab the latest lightning data from the database ans store locally.

    Liam.Buchart@NRcan-RNcan.gc.ca
    August 5, 2026

"""
#%%
import json
import psycopg2
import paramiko
import json
import csv
import sshtunnel
import sys
import os

import pandas as pd

from sshtunnel import SSHTunnelForwarder

from UTILS.file_funcs import db_query, cldn_query
from context import download_dir

# %%
query = cldn_query()
print(query)

db_query(query, csv_output=f"{download_dir}/lightning_data.csv")
# %%
