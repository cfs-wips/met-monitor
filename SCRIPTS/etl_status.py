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
# get all files in the local download directory that have *status* in the name
status_files_local = [f for f in os.listdir(local_file) if "status" in f]

def parse_status_csv(path):
    """Parse a status file into a DataFrame with date, records, and 2-digit hour columns."""
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline().strip().split()
        if len(header) < 3:
            raise ValueError(f"Unexpected header line format: {header}")

        records_code = header[1]
        time_header = header[2]
        hour_cols = [time_header[i : i + 2] for i in range(0, len(time_header), 2)]

        records = []
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            date = parts[0]
            values = parts[1]
            value_cols = [values[i : i + 2] for i in range(0, len(values), 2)]
            if len(value_cols) != len(hour_cols):
                value_cols = value_cols[: len(hour_cols)] + [None] * max(0, len(hour_cols) - len(value_cols))

            if idx == 0:
                row = [date, records_code] + value_cols
            else:
                row = [date, None] + value_cols

            records.append(row)

    columns = ["date", "records"] + hour_cols
    return pd.DataFrame(records, columns=columns)

#%%
# want to save these csv files in a better format to have individual columns for each hour status percentage
for file in status_files_local:
    if "provwxc" in file:
        print(f"Skipping file: {file}")
        continue
    else:

        file_path = os.path.join(local_file, file)
        print(f"Processing file: {file}")
        df = parse_status_csv(file_path)
        print(df.shape)
        print(df.head())
        # save the dataframe to a new csv file with the same name but in the download directory
        df.to_csv(os.path.join(local_file, f"{file}"), index=False)
print("All status files processed and saved...")
# %%
