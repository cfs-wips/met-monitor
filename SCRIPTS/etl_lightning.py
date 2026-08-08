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

file_name = f"{download_dir}/lightning_data.csv"

db_query(query, csv_output=file_name)

# open the csv and remove headers for a final save
df = pd.read_csv(file_name)
df.to_csv(file_name, index=False, header=False)
# %%
