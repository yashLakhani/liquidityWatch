from sqlalchemy import create_engine
from instance.config import DB_URL
from app.modules.setup.pg_helper import psql_insert_copy
import pandas as pd
import requests, zipfile, io, os


def download_metadata(dataset_name):
    req = 'https://www.quandl.com/api/v3/databases/{}/metadata'.format(dataset_name)
    r = requests.get(req)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('data')


def parse_instruments(filename):
    instrument_df = pd.read_csv(filename)
    instrument_details = instrument_df["code"].str.split("_", n=1, expand=True)
    instrument_df["exchange"] = instrument_details[0]
    instrument_df["code"] = instrument_details[1]
    instrument_df.drop(columns=["description"], inplace=True)
    return instrument_df


def load_instruments(dataset_name, filename):
    download_metadata(dataset_name)
    instruments_df = parse_instruments(filename)
    engine = create_engine(DB_URL)
    instruments_df.to_sql('instrument', engine, if_exists='replace', method=psql_insert_copy)


if __name__ == "__main__":
    if os.name == 'nt':
        filename = 'data\CHRIS_metadata.csv'
    else:
        filename = 'data/CHRIS_metadata.csv'

    load_instruments('CHRIS', filename)
