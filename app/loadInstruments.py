from instance.config import API_KEYS
import quandl
import requests
import pandas as pd
import numpy as np
import requests, zipfile, io
import psycopg2

pd.set_option('display.max_columns', None)
pd.set_option('max_rows',3000)
pd.set_option('max_colwidth', 200)
pd.set_option('display.max_columns', 150)
pd.set_option('display.width', 1000)

quandl.ApiConfig.api_key = API_KEYS['QUANDL_API_KEY']


def download_metadata(dataset_name):
    req = 'https://www.quandl.com/api/v3/databases/{}/metadata'.format(dataset_name)
    r = requests.get(req)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()


def load_instruments(filename):
    instrument_df = pd.read_csv(filename)
    instrument_details = instrument_df["code"].str.split("_", n=1, expand=True)
    instrument_df["exchange"] = instrument_details[0]
    instrument_df["code"] = instrument_details[1]
    instrument_df.drop(columns=["description"], inplace=True)
    print(instrument_df.head())
    return instrument_df
    #df.to_sql('', engine)




download_metadata('CHRIS')
instruments_df = load_instruments('CHRIS_metadata.csv')

from sqlalchemy import create_engine
from dataManipulation import psql_insert_copy

engine = create_engine('postgresql://localhost/wikidb')
instruments_df.to_sql('instrument', engine, method=psql_insert_copy)