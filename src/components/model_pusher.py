import os
import json
import tensorflow as tf
from src.entity.artifact_entity import DataTransformationArtifact, ModelEvaluatorArtifact
from src.utils.utils import load_and_split_data
from src.utils.s3_operation_utils import S3_operation
from sklearn.metrics import accuracy_score
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

        self.s3_operation = S3_operation()
        print(self.s3_operation.accessing_path_s3(PREPROCESS_MODEL_PATH))
        print(self.s3_operation.accessing_path_s3(S3_NEW_VERSION))

    def uploading_process_pkl(self):
        local_file = os.listdir(self.process_model_dir)[0]
        s3_files = self.s3_operation.accessing_path_s3(PREPROCESS_MODEL_PATH)

        process_pkl_path = os.path.join(self.process_model_dir, local_file)
        process_model_key = f"{PREPROCESS_MODEL_PATH}/{local_file}"

        if process_model_key in s3_files:
            self.s3_operation.delete_file(process_model_key)
            logging.info(f"Existing {os.path.basename(process_model_key)} file deleted from S3: {process_model_key}")

        self.s3_operation.upload_file(process_pkl_path, process_model_key)
        logging.info(f"New {local_file} uploaded to S3: {process_model_key}")

        return process_model_key
    
    def evaluate_model_accuracy(self, model, x_test, y_test):
        y_pred = model.predict(x_test)
        y_pred_prob = (y_pred > 0.5).astype(int)
        accuracy = accuracy_score(y_test, y_pred_prob)
        return accuracy
    
    def checking_accuracy(self):
        local_model = tf.keras.models.load_model(self.model_path)
        
        s3_model_path = self.s3_operation.accessing_path_s3(S3_NEW_VERSION)[0]
        s3_model = self.s3_operation.load_model(s3_model_path)

        _, _, X_test, y_test = load_and_split_data(self.x, self.y)
        s3_accuracy = round(self.evaluate_model_accuracy(s3_model, X_test, y_test), 4)
        local_accuracy = round(self.evaluate_model_accuracy(local_model, X_test, y_test), 4)

        return s3_accuracy, local_accuracy
        
    def upload_or_reject_model(self):
        s3_model_paths = self.s3_operation.accessing_path_s3()

        if not s3_model_paths:  
            new_model_key = f"{S3_NEW_VERSION}/{os.path.basename(self.model_path)}"
            self.s3_operation.upload_file(self.model_path, new_model_key)
            logging.info(f"No model found in S3. Uploading new model to S3: {new_model_key}")
            return new_model_key

        s3_model_path = s3_model_paths[0]  
        s3_accuracy, local_accuracy = self.checking_accuracy()
        
        if s3_accuracy is not None and local_accuracy is not None:
            if local_accuracy > s3_accuracy:
                old_model_key = f"{S3_OLDER_VERISON}/{os.path.basename(s3_model_path)}"
                self.s3_operation.copy_file(s3_model_path, old_model_key)
                self.s3_operation.delete_file(s3_model_path)
                logging.info(f"S3 model moved {os.path.basename(s3_model_path)} to older version: {old_model_key}")
                logging.info(f"New model accuracy ({local_accuracy}) is higher than S3 model accuracy ({s3_accuracy}). "
                            "Uploading new model and moving S3 model to older version folder.")
                new_model_key = f"{S3_NEW_VERSION}/{os.path.basename(self.model_path)}"
                self.s3_operation.upload_file(self.model_path, new_model_key)
                logging.info(f"New model uploaded to S3: {new_model_key}")
                return new_model_key
            else:
                logging.info(f"New model accuracy ({local_accuracy}) is not higher than S3 model accuracy ({s3_accuracy}). "
                            "Rejecting the new model.")
                return s3_model_path
        else:
            logging.warning("New accuracy or S3 accuracy not provided. Unable to compare models.")
            return s3_model_path



    def initiate_model_pusher(self):
        logging.info("============================================================================")
        logging.info("=========================  Start MODEL Pusher into S3 BUcket ==============")
        process_path = self.uploading_process_pkl()
        model_path = self.upload_or_reject_model()

        model_info = {
            "process_path": process_path,
            "model_path": model_path
        }
        json_path = os.path.join(CONFIG_DIR_NAME, MODEL_REPORT_FILE_NAME)
        with open(json_path, "w") as json_file:
            json.dump(model_info, json_file)
        logging.info("=========================   MODEL Pusher Completed... ==============")
        


# import os
# import json
# import tensorflow as tf
# from src.entity.artifact_entity import DataTransformationArtifact, ModelEvaluatorArtifact
# from src.utils.utils import load_and_split_data
# from src.utils.s3_operation_utils import S3_operation
# from sklearn.metrics import accuracy_score
# from src.logger import logging
# from src.constant.constants import *

# class ModelLoader:
#     def __init__(self,
#                  data_transform_artifact: DataTransformationArtifact,
#                  model_evaluation_artifact: ModelEvaluatorArtifact
#                  ):
#         self.x = data_transform_artifact.feature_data_file_path
#         self.y = data_transform_artifact.label_data_file_path
#         self.process_model_dir = data_transform_artifact.preprocess_file_path

#         self.process_model = data_transform_artifact.preprocess_file_path
#         self.model_path = model_evaluation_artifact.accepted_model_path

#         self.s3_operation = S3_operation()
#         print(self.s3_operation.accessing_path_s3(PREPROCESS_MODEL_PATH))
#         print(self.s3_operation.accessing_path_s3(S3_NEW_VERSION))

#     def uploading_process_pkl(self):
#         local_file = os.listdir(self.process_model_dir)[0]
#         s3_files = self.s3_operation.accessing_path_s3(PREPROCESS_MODEL_PATH)

#         process_pkl_path = os.path.join(self.process_model_dir, local_file)
#         process_model_key = f"{PREPROCESS_MODEL_PATH}/{local_file}"

#         if process_model_key in s3_files:
#             self.s3_operation.delete_file(process_model_key)
#             logging.info(f"Existing {os.path.basename(process_model_key)} file deleted from S3: {process_model_key}")

#         self.s3_operation.upload_file(process_pkl_path, process_model_key)
#         logging.info(f"New {local_file} uploaded to S3: {process_model_key}")

#         return process_model_key
    
#     def evaluate_model_accuracy(self, model, x_test, y_test):
#         y_pred = model.predict(x_test)
#         y_pred_prob = (y_pred > 0.5).astype(int)
#         accuracy = accuracy_score(y_test, y_pred_prob)
#         return accuracy
    
#     def checking_accuracy(self):
#         local_model = tf.keras.models.load_model(self.model_path)
        
#         s3_model_path = self.s3_operation.accessing_path_s3(S3_NEW_VERSION)[0]
#         s3_model = self.s3_operation.load_model(s3_model_path)

#         _, _, X_test, y_test = load_and_split_data(self.x, self.y)
#         s3_accuracy = round(self.evaluate_model_accuracy(s3_model, X_test, y_test), 2)
#         local_accuracy = round(self.evaluate_model_accuracy(local_model, X_test, y_test), 2)

#         return s3_accuracy, local_accuracy
        
#     def upload_or_reject_model(self, new_accuracy, s3_accuracy=None):
#         s3_model_path = self.s3_operation.accessing_path_s3(S3_NEW_VERSION)[0]

#         if new_accuracy > s3_accuracy:
#             old_model_key = f"{S3_OLDER_VERISON}/{os.path.basename(s3_model_path)}"
#             self.s3_operation.copy_file(s3_model_path, old_model_key)
#             self.s3_operation.delete_file(s3_model_path)
#             logging.info(f"S3 model moved {os.path.basename(s3_model_path)} to older version: {old_model_key}")
#             logging.info(f"New model accuracy ({new_accuracy}) is higher than S3 model accuracy ({s3_accuracy}). "
#                         "Uploading new model and moving S3 model to older version folder.")
#             new_model_key = f"{S3_NEW_VERSION}/{os.path.basename(self.model_path)}"
#             self.s3_operation.upload_file(self.model_path, new_model_key)
#             logging.info(f"New model uploaded to S3: {new_model_key}")
#             return new_model_key
#         else:
#             logging.info(f"New model accuracy ({new_accuracy}) is not higher than S3 model accuracy ({s3_accuracy}). "
#                         "Rejecting the new model.")
#             return s3_model_path

#     def initiate_model_pusher(self):
#         process_path = self.uploading_process_pkl()
#         s3_accuracy, local_accuracy = self.checking_accuracy()

#         model_path = self.upload_or_reject_model(s3_accuracy, local_accuracy)

#         model_info = {
#             "process_path": process_path,
#             "model_path": model_path
#         }
#         json_path = os.path.join(CONFIG_DIR_NAME, MODEL_REPORT_FILE_NAME)
#         with open(json_path, "w") as json_file:
#             json.dump(model_info, json_file)
