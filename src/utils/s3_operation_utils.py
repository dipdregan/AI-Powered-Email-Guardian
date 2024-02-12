import boto3
import tensorflow as tf
import joblib
import os
from dotenv import load_dotenv
from src.constant.constants import *

class S3_operation:
    def __init__(self):
        load_dotenv()
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION')
        self.bucket_name = BUCKET_NAME
        self.s3_new_version = S3_NEW_VERSION
        self.s3_older_version = S3_OLDER_VERISON
        self.s3_client = boto3.client('s3', aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key,
                                      region_name=self.aws_region)
        
    def accessing_path_s3(self, model_path):
        file_paths = []
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name,
                                                  Prefix=model_path + '/')
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):
                    file_paths.append(obj['Key'])
        return file_paths
    
    def load_model(self, model_key):
        local_model_path = "model.h5"  
        self.s3_client.download_file(self.bucket_name, model_key, local_model_path)
        model = tf.keras.models.load_model(local_model_path)
        os.remove(local_model_path)
        return model
    
    def load_process_model(self, model_key):
        local_process_path = "process.pkl"
        self.s3_client.download_file(self.bucket_name, model_key, local_process_path)
        process_model = joblib.load(local_process_path)
        os.remove(local_process_path)
        return process_model

    def upload_file(self, local_file_path, s3_key):
        with open(local_file_path, "rb") as file:
            self.s3_client.upload_fileobj(file, self.bucket_name, s3_key)

    def delete_file(self, s3_key):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        
    def copy_file(self, source_key, destination_key):
        copy_source = {'Bucket': self.bucket_name, 'Key': source_key}
        self.s3_client.copy_object(CopySource=copy_source, Bucket=self.bucket_name, Key=destination_key)
