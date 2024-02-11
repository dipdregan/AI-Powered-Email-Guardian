import boto3
from tensorflow.keras.models import load_model
from io import BytesIO
from dotenv import load_dotenv
from src.entity.artifact_entity import DataTransformationArtifact, ModelEvaluatorArtifact
from src.utils.utils import load_and_split_data
from sklearn.metrics import accuracy_score
import os
from src.logger import logging
from src.constant.constants import *

class ModelLoader:
    def __init__(self,
                 data_transform_artifact: DataTransformationArtifact,
                 model_evaluation_artifact: ModelEvaluatorArtifact
                 ):
        self.x = data_transform_artifact.feature_data_file_path
        self.y = data_transform_artifact.label_data_file_path
        self.process_model_dir = data_transform_artifact.preprocess_file_path

        self.process_model = data_transform_artifact.preprocess_file_path
        self.model_path = model_evaluation_artifact.accepted_model_path


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
        
    def uploading_process_pkl(self):
        if os.path.exists(self.process_model_dir):
            files = os.listdir(self.process_model_dir)
            if "preprocess.pkl" in files:
                process_pkl_path = os.path.join(self.process_model_dir, "preprocess.pkl")
                process_model_key = f"{self.s3_new_version}/preprocess.pkl"
                
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=process_model_key)
                logging.info(f"Existing process.pkl file deleted from S3: {process_model_key}")

                with open(process_pkl_path, "rb") as process_pkl_file:
                    self.s3_client.upload_fileobj(process_pkl_file,
                                                self.bucket_name, 
                                                process_model_key)
                logging.info(f"New process.pkl uploaded to S3: {process_model_key}")
            else:
                logging.info("No process.pkl file found in the process model directory.")
        else:
            logging.error("Process model directory does not exist.")


    def load_model_from_s3_new(self, model_key):
        local_model_path = "model.h5"  
        self.s3_client.download_file(self.bucket_name, model_key, local_model_path)
        s3_model = load_model(local_model_path)
        new_model = load_model(self.model_path)
        os.remove(local_model_path)
        return s3_model, new_model

    def accessing_path_s3(self):
        file_paths = []
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name,
                                                  Prefix=self.s3_new_version + '/')
        if 'Contents' in response:
            for obj in response['Contents']:
                if not obj['Key'].endswith('/'):
                    file_paths.append(obj['Key'])
        logging.info(f"S3 bucket files accessed successfully. {file_paths}")
        return file_paths
    
    def evaluate_model_accuracy(self, model, x_test, y_test):
        y_pred = model.predict(x_test)
        y_pred_prob = (y_pred > 0.5).astype(int)
        accuracy = accuracy_score(y_test, y_pred_prob)
        return accuracy

    def compare_models_update_models(self, s3_model, new_model, x_test, y_test):
        s3_model_accuracy = self.evaluate_model_accuracy(s3_model, x_test, y_test)
        new_model_accuracy = self.evaluate_model_accuracy(new_model, x_test, y_test)

        print(f"S3 model_acc : {s3_model_accuracy}")
        print(f"new model_Accu :{new_model_accuracy}")
        model_name = os.path.basename(self.model_path)
        old_model_key = self.accessing_path_s3()[0]  
        old_model_name = os.path.basename(old_model_key)

        if new_model_accuracy > s3_model_accuracy:
            logging.info(f"New model {model_name} has higher accuracy {new_model_accuracy} in comparison to model {old_model_name} with accuracy {s3_model_accuracy}. Uploading to S3...")
            model_path = f"{self.s3_new_version}/{model_name}"
            
            # Upload new model to S3
            new_model.save(model_name)
            with open(model_name, "rb") as model_file:
                self.s3_client.upload_fileobj(model_file, self.bucket_name, model_path)
            logging.info(f"Model uploaded to S3: {model_path}")
            logging.info(f"less acc Model{old_model_name} move to s3 {self.s3_older_version}")
            
            old_model_old_version_key = old_model_key.replace(self.s3_new_version, self.s3_older_version)
            copy_source = {'Bucket': self.bucket_name, 'Key': old_model_key}
            self.s3_client.copy_object(CopySource=copy_source, Bucket=self.bucket_name, Key=old_model_old_version_key)
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=old_model_key)
            logging.info(f"Old model moved to older version: {old_model_old_version_key}")

        else:
            logging.info(f"S3 model {model_name} has higher or equal accuracy {s3_model_accuracy} in comparison to model {model_name} with accuracy {new_model_accuracy}. Not updating.")

    def initiate_model_pusher(self):
        file_paths = self.accessing_path_s3()
        if not file_paths:
            logging.info("No models found in S3. Pushing the model to the 'New_version_model' folder.")
            # Assuming self.model_path contains the path to the model you want to push
            model_name = os.path.basename(self.model_path)
            model_path = f"{self.s3_new_version}/{model_name}"
            new_model = load_model(self.model_path)
            new_model.save(model_name)
            with open(model_name, "rb") as model_file:
                self.s3_client.upload_fileobj(model_file, self.bucket_name, model_path)
            logging.info(f"Model uploaded to S3: {model_path}")
            
            return {
                "model": new_model,
                "model_key": model_path,
                "model_accuracy": None  # Since we don't have accuracy without evaluation
            }
        
        s3_model_key = file_paths[0]
        s3_model, new_model = self.load_model_from_s3_new(s3_model_key)

        _, _, x_test, y_test = load_and_split_data(self.x, self.y)
        self.compare_models_update_models(s3_model, new_model, x_test, y_test)

        return {
            "model": new_model,
            "model_key": s3_model_key,
            "model_accuracy": self.evaluate_model_accuracy(new_model, x_test, y_test)
        }


