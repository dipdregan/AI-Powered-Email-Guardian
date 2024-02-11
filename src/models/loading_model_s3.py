import boto3
import os
import joblib
from dotenv import load_dotenv
from src.constant.constants import *

load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
bucket_name = BUCKET_NAME
s3_new_version = S3_NEW_VERSION
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key,
                                      region_name=aws_region)

def accessing_path_s3(self):
    file_paths = []
    response = s3_client.list_objects_v2(Bucket=bucket_name,
                                              Prefix=s3_new_version + '/')
    if 'Contents' in response:
        for obj in response['Contents']:
            if not obj['Key'].endswith('/'):
                file_paths.append(obj['Key'])
    return file_paths

def load_model(model_key):
    local_model_path = "model.h5"  
    s3_client.download_file(bucket_name, model_key, local_model_path)
    model = load_model(local_model_path)
    os.remove(local_model_path)
    return model

def load_process_model(model_key):
    local_process_path = "process.pkl"
    s3_client.download_file(bucket_name, model_key, local_process_path)
    process_model = joblib.load(local_process_path)
    os.remove(local_process_path)
    return process_model
