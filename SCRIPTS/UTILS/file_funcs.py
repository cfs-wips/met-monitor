import json
import psycopg2
import paramiko
import csv
import sshtunnel
import os

import pandas as pd

from datetime import datetime, timedelta
from sshtunnel import SSHTunnelForwarder

def db_query(query, csv_output='query_output.csv'):
    """
    Call the database to get wind data
    Inut: cursor object (defined below)
          start and end [dates YYYY-MM-DD - string]
    Output: pandas dataframe
    """
    # open the .keys json file
    with open('./.dagan_keys.json', 'r') as f:
        keys = json.load(f)

    # dagan info
    hostname = keys["dagan"]["full_name"]
    user = keys["dagan"]["user"]
    #pw = keys["dagan"]["pw"]
    pw = input(f"Enter password for {user}@{hostname}: ")

    # database info
    d_hostname = keys["database"]["hostname"]
    d_username = keys["database"]["user"]
    db_name = keys["database"]["name"]
    #d_pw = keys["database"]["pw"]
    d_pw = input(f"Enter password for db: -U {d_username} -d {d_hostname} -h {db_name}: ")

    portnum = 22  # just lookedup in my putty session

    # connect to remote database
    with sshtunnel.open_tunnel(
        (hostname, portnum),
        ssh_username=user,
        ssh_password=pw,
        remote_bind_address=(d_hostname, 5432)
    ) as tunnel:
        try:
            print("SSH tunnel established")
            print(f"{d_hostname, tunnel.local_bind_port}")
            print(f"Connecting to database {db_name} as user {d_username}")
            conn = psycopg2.connect(
                host=d_hostname,
                port=5432,
                database=db_name,
                user=d_username,
                password=d_pw
            )  

            cur = conn.cursor()
            # start by setting the search path
            cur.execute("set search_path to bt;")
            cur.execute(query)
            rows = cur.fetchall()  

            colnames = [desc[0] for desc in cur.description]
            with open(csv_output, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(colnames)
                writer.writerows(rows)
            cur.close()
            conn.close()

            print(f"Query results saved to {csv_output}")

        except Exception as e:
            print("Error:", e)

def cldn_query():
    # grab the most recent 25 stikes that we will display on the site
    q1 = f"SELECT rep_date, lat, lon, peak_current, mult_flash FROM cldn_strikes "
    q2 = f"ORDER BY rep_date DESC LIMIT 25;"

    return q1 + q2

def db_copy_status(status_path, download_path):
    # ssh into the desired system and copy files from the path variable (status files to be displayed)
        # open the .keys json file
    with open('./.dagan_keys.json', 'r') as f:
        keys = json.load(f)

    # dagan info
    hostname = keys["dagan"]["full_name"]
    user = keys["dagan"]["user"]
    #pw = keys["dagan"]["pw"]
    pw = input(f"Enter password for {user}@{hostname}: ")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, username=user, password=pw)
    print(f"Connected to {hostname} as {user}")

    sftp_client = ssh_client.open_sftp()

    files = sftp_client.listdir(status_path)
    print("Files and directories:", files)

    for file in files:
        remote_file_path = os.path.join(status_path, file)
        local_file_path = os.path.join(download_path, f"{file}.csv")
        sftp_client.get(remote_file_path, local_file_path)
        print(f"Copied {remote_file_path} to {local_file_path}")

    #sftp_client.get(status_path, download_path)

    sftp_client.close()
    ssh_client.close()

    return files