
from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import boto3
import uuid
import os

# Replace 'your_aws_region' with the actual AWS region of your S3 bucket
region_name = 'eu-west-1'
S3_GENERATED_CONTRACTS = 'generated-orima-law-contracts'
S3_CONTRACT_TEMPLATES = 'orima-contract-templates'

# Create a Boto3 S3 client
s3_client = boto3.client('s3', region_name=region_name)

def download_contract(contract_name):
    # Replace 'your_bucket_name' with the name of your S3 bucket
    bucket_name = 'orima-contract-templates'

    # Replace 'your_object_key' with the key (path) of the file you want to download from the bucket
    object_key = contract_name

    # Replace 'your_local_file_path' with the path where you want to save the downloaded file locally
    local_file_path = contract_name

    try:
        s3_client.download_file(bucket_name, object_key, local_file_path)
        print(f"File downloaded successfully to: {local_file_path}")
    except Exception as e:
        print("Error:", e)

#Send a document to s3
def upload_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded {file_path} to S3 bucket {bucket_name} as {object_name}")
        os.remove(file_path)
    except Exception as e:
        print(f"Error uploading {file_path} to S3 bucket {bucket_name}: {str(e)}")

def generate_contract(data):

    contract_name = data['contract_name']
    download_contract(contract_name)

    document = MailMerge(contract_name)
    merge_fields = document.get_merge_fields()
    map = {}
    for field in merge_fields:
        map[field] = data[field]

    document.merge(**map)
    
    # Generate a random UUID (UUID version 4)
    unique_id = uuid.uuid4()
    WORD_DOCUMENT_PATH = f'{contract_name}-{unique_id}.docx'
    document.write(WORD_DOCUMENT_PATH)

    s3_folder_path = f'{contract_name}/{unique_id}.docx'     # Replace with the desired folder path in S3
    
    
    # Upload the Word document
    upload_to_s3(WORD_DOCUMENT_PATH, S3_GENERATED_CONTRACTS, s3_folder_path)
    # Assuming 'generated_document_key' is the object key in your S3 bucket
    generated_document_key = s3_folder_path

    # Generate a pre-signed URL for the S3 object
    document_url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': S3_GENERATED_CONTRACTS, 'Key': generated_document_key},
                                                    ExpiresIn=3600)  # URL will be valid for 1 hour (3600 seconds)

    return document_url