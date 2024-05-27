import requests
import pandas as pd
from zipfile import ZipFile
import io
from sqlalchemy import create_engine

# PostgreSQL connection parameters
DB_USER = 'clab'
DB_PASSWORD = 'clab'
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
DB_NAME = 'Email_db'

# Kaggle REST endpoint for the zipped data
KAGGLE_ZIP_URL = 'https://storage.googleapis.com/kaggle-data-sets/5052569/8473333/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20240527%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20240527T131307Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=7d482d621c39d9e6c24c22f92ac1c907d8ea342c1cdb8ac003f69ae9efbef64ddea7266a400cdec84a7ad6ae97f819f58c7ee93b963d116bda2d1ecb119ebe3f529eff5511af6b65b8d42b3a76e4cd25a02ac73f85a6333c14d0b2486603299b004f7f73f88a5969725bd97a7a45439ce8f6566ef5a9407f78d642ac12ceafff16f3c5c3a13b782076549198ca8d519cee3e9900d0e64378afad18dfaaeecaefe598f40329ebc5c9b99f60387f240c0a8d9d78058091b90275b293f8d410bedd95fe00341566f63c16f6decfcc37850e8f41eb6e993490cfc8368c07ef04bd6977098d2d34525ae9fded2ba51450a5a4ba8fb27ed6287ba6373a03b1ddc6b7ec'  # Replace with actual endpoint

def fetch_and_extract_data():
    try:
        response = requests.get(KAGGLE_ZIP_URL)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        # Extract the zip file contents into memory
        with ZipFile(io.BytesIO(response.content)) as zip_file:
            # Assuming there's only one file in the zip archive
            file_name = zip_file.namelist()[0]
            with zip_file.open(file_name) as extracted_file:
                data = extracted_file.read()
        return data
    except Exception as e:
        print(f"Error fetching and extracting data: {e}")
        return None

def populate_db(data):
    try:
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        df = pd.read_csv(io.BytesIO(data))  # Assuming the data is in CSV format
        df.to_sql('ClientData', engine, if_exists='replace', index=False)
        print("Data populated into the database successfully.")
    except Exception as e:
        print(f"Error populating data into the database: {e}")

if __name__ == "__main__":
    data = fetch_and_extract_data()
    if data:
        populate_db(data)
