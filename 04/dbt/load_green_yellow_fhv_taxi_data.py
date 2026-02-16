
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time


# Change this to your bucket name
BUCKET_NAME = "dwh-trip-data"

client = storage.Client(project='endless-office-485017-f8')

# The URL template for NYC Taxi data releases
URL_TEMPLATE = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{color}_tripdata_{year}-{month}.csv.gz"
COLOR_LIST = ["yellow", "green", "fhv"]
YEAR_LIST = ["2019", "2020"]
MONTH_LIST = [f"{i:02d}" for i in range(1, 13)]
DOWNLOAD_DIR = "data"

CHUNK_SIZE = 8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)


def download_file(color, year, month):
    url = URL_TEMPLATE.format(color=color, year=year, month=month)
    file_name = f"{color}_tripdata_{year}-{month}.csv.gz"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    try:
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return file_path

        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def create_bucket(bucket_name):
    try:
        # Get bucket details
        client.get_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' exists. Proceeding...")
    except NotFound:
        # If the bucket doesn't exist, create it
        client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden:
        print(f"Access to bucket '{bucket_name}' is forbidden. Please check your permissions or use a different bucket name.")
        sys.exit(1)


def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


def process_file(args):
    color, year, month = args
    file_path = download_file(color, year, month)
    if file_path:
        upload_to_gcs(file_path)


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    tasks = []
    for color in COLOR_LIST:
        for year in YEAR_LIST:
            for month in MONTH_LIST:
                tasks.append((color, year, month))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_file, tasks)

    print("All files processed and verified.")
