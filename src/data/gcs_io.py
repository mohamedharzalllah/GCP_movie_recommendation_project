from google.cloud import storage


class GCSWriter:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_dataframe_parquet(self, df, gcs_path: str):
        tmp_file = "/tmp/data.parquet"
        df.to_parquet(tmp_file, index=False)

        blob = self.bucket.blob(gcs_path)
        blob.upload_from_filename(tmp_file)

        print(f"Uploaded to gs://{self.bucket.name}/{gcs_path}")
from google.cloud import storage
import pandas as pd
import tempfile
import os


class GCSReader:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def read_parquet(self, gcs_path: str) -> pd.DataFrame:
        blob = self.bucket.blob(gcs_path)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".parquet") as tmp:
            blob.download_to_filename(tmp.name)
            df = pd.read_parquet(tmp.name)

        os.remove(tmp.name)
        return df
