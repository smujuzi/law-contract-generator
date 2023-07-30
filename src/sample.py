
from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import boto3
import uuid
import os




# Your AWS S3 credentials and bucket name
AWS_ACCESS_KEY = 'AKIA3G3ULJIT7OPEFOAV'
AWS_SECRET_KEY = 'yV3etsUyiwOJcHY41UlJ9PjYqQyFxCxztLnF01lU'
S3_BUCKET_NAME = 'generated-orima-law-contracts'


# Create an S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

template = "draft-spousal-consent.docx"



people = [
    {
        "spouse_name": "Stuart",
        "spouse_address": "Bristol",
        "borrowers_lawyer": "James"
    },
    {
        "spouse_name": "Kizito",
        "spouse_address": "Kawempe",
        "borrowers_lawyer": "Bosco"
    },
    {
        "spouse_name": "Sanyu",
        "spouse_address": "Wandegeya",
        "borrowers_lawyer": "Ssebagala"
    },
    {
        "spouse_name": "Richard",
        "spouse_address": "Ntinda",
        "borrowers_lawyer": "Antoinette"
    },
]

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

print('...Generating contracts')
for ob in people:
    document = MailMerge(template)
    print(document.get_merge_fields())
    document.merge(
        spouse_name = ob["spouse_name"],
        spouse_address = ob["spouse_address"],
        borrowers_lawyer = ob["borrowers_lawyer"]
        )
    #s3_folder_path = 'folder/subfolder/file.txt'     # Replace with the desired folder path in S3
    
    # Generate a random UUID (UUID version 4)
    unique_id = uuid.uuid4()
    print(unique_id)
    WORD_DOCUMENT_PATH = f'{template}-{unique_id}'
    document.write(WORD_DOCUMENT_PATH)
    s3_folder_path = f'{template}/{unique_id}.docx'     # Replace with the desired folder path in S3
    # Upload the Word document
    upload_to_s3(WORD_DOCUMENT_PATH, S3_BUCKET_NAME, s3_folder_path)
    # Assuming 'generated_document_key' is the object key in your S3 bucket
    generated_document_key = s3_folder_path

    # Generate a pre-signed URL for the S3 object
    document_url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': S3_BUCKET_NAME, 'Key': generated_document_key},
                                                    ExpiresIn=3600)  # URL will be valid for 1 hour (3600 seconds)

    print('Document URL:', document_url)
