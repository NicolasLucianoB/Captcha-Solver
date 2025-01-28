import os

import boto3
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve credentials and configuration from environment variables
access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")
bucket_name = os.getenv("BUCKET_NAME")
endpoint_url = os.getenv("ENDPOINT_URL")

# Initialize the S3 client with the credentials and endpoint URL
s3_client = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# Local directory to store downloaded images
output_folder = './imagens'
os.makedirs(output_folder, exist_ok=True)  # Ensure the directory exists

# Count the number of files in the "imagens" folder
num_files = len(os.listdir(output_folder))
print(f"Number of files in the 'imagens' folder: {num_files}")

# Name of the last downloaded file (used as a reference point)
last_downloaded = '20241015004258'

# Paginate through the S3 bucket to list and download new files
continuation_token = None
while True:
    # Fetch a page of results with or without a continuation token
    if continuation_token:
        objects = s3_client.list_objects_v2(Bucket=bucket_name, ContinuationToken=continuation_token)
    else:
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Process the files listed in the current page
    if 'Contents' in objects:
        for obj in objects['Contents']:
            key = obj['Key']
            if key > last_downloaded:  # Compare filenames to filter new files
                file_path = os.path.join(output_folder, key)
                try:
                    print(f"Downloading {key} to {file_path}")
                    # Download the file from the bucket to the local directory
                    s3_client.download_file(bucket_name, key, file_path)
                except Exception as e:
                    print(f"Error downloading {key}: {e}")
    
    # Check if there are more pages of results to process
    if objects.get('IsTruncated'):  # Indicates if there are more results
        continuation_token = objects['NextContinuationToken']
        print("Moving to the next page of results...")
    else:
        print("All files have been processed.")
        break