""" 

    Grab all the current status files for all process and store copy locally

    Liam.Buchart@NRCan-RNCan.gc.ca
    August 6, 2026

"""
#%%
import json
import psycopg2
import paramiko
import csv
import sshtunnel
import sys
import os

import pandas as pd

from sshtunnel import SSHTunnelForwarder

from UTILS.file_funcs import db_copy_status
from context import download_dir, utils_dir

#%%
with open(f'{utils_dir}/dagan_paths.json', 'r') as f:
    paths = json.load(f)

status_path = paths["status"]   
print(status_path + "*") 

local_file = f"{download_dir}"

# need to get all the names of files in the status path, 
# then loop through files and copy each one over inidivually

#%%
# copy over all status files
status_files = db_copy_status(f"{status_path}", local_file)
# %%
