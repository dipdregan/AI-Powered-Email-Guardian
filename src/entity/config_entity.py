from datetime import datetime
from src.constant.constants import *
import os 

class RootConfig:

    def __init__(self):
        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.artifact_dir: str = os.path.join(ARTIFACT_DIR, timestamp)
        self.timestamp: str = timestamp

class DataIngestionConfig:

    def __init__(self, root_dir: RootConfig):
        self.data_ingestion_dir: str = os.path.join(root_dir.artifact_dir,
                                                    DATA_INGETION_DIR_NAME)
        #artifact/timestamp/data_ingetion

        self.kaggle_data_zip_file_path: str = os.path.join(self.data_ingestion_dir,
                                                           DATA_INGETION_KAGGLE_DATA_STORE_DIR)
        #artifact/timestamp/data_ingetion/zip_dir

        self.unzip_file_path: str = os.path.join(self.data_ingestion_dir,
                                                 DATA_INGETION_UNZIP_DATA_STORE_DIR)
        #artifact/timestamp/data_ingetion/unzip_dir

        self.data_api: str = Data_API
        

class DataValidationConfig:
    def __init__(self,root_dir:RootConfig):
        self.data_validation_dir:str = os.path.join(root_dir.artifact_dir,
                                                    DATA_VALIDATION_DIR_NAME)
        
        self.data_validation_validate_path:str = os.path.join(self.data_validation_dir,
                                                              DATA_VALIDATION_VALID_DIR,
                                                              )
        self.valide_data_file_name:str = DATA_VALIDATION_VALID_FILE_NAME
        
        self.data_validation_invalidate_path:str = os.path.join(self.data_validation_dir,
                                                                DATA_VALIDATION_INVALID_DIR,
                                                                )
        
        self.invalide_data_file_name:str = DATA_VALIDATION_INVALID_FILE_NAME
        
        self.data_validation_report_path:str = os.path.join(self.data_validation_dir,
                                                       DATA_VALIDATION_REPORT_FILE_PATH)
        
        self.report_file_name:str = DATA_VALIDATION_REPORT_FILE_NAME
        self.data_types:dict = CONFIG_FILE['columns_data_type']
        self.expected_columns:list = CONFIG_FILE['columns']

class DataTransformationConfig:
    def __init__(self, root_dir:RootConfig):
        self.data_transformation_dir:str = os.path.join(root_dir.artifact_dir,
                                                        DATA_TRANSFORMATION_DIR_NAME)
        
        self.transform_dir_path:str = os.path.join(self.data_transformation_dir,
                                                   TRASNFORM_DATA_DIR_NAME)


        self.feature_data_file_path:str = os.path.join(self.data_transformation_dir,
                                                  FEATURE_TARGET_DATA_DIR_NAME)
        
        self.preprocess_model_file_path:str = os.path.join(self.data_transformation_dir,
                                                           PREPROCESS_DATA_DIR_NAME)
        

class ModelTrainerConfig:
        
    def __init__(self, root_dir:RootConfig):
        self.model_trainer_dir : str = os.path.join(root_dir.artifact_dir, MODEL_TRAINER)
        self.model_dir:str = os.path.join(self.model_trainer_dir,MODEL_DIR) 
    
        self.training_history_dir = os.path.join(self.model_trainer_dir,
                                                 TRAINING_HISTORY_DIR)
        self.training_history_file_name = TRAINING_HISTORY_FILE_NAME
        
        self.training_report = os.path.join(self.model_trainer_dir,
                                              TRAINING_ACC_LOSS_SCORE)
        

class ModelEvaluatorConfig:
    def __init__(self, root_dir: RootConfig):
        self.model_evaluator_dir = os.path.join(MODEL_EVALUATOR_DIR_NAME)  
        
        self.accepted_model = os.path.join(self.model_evaluator_dir,
                                           ACCEPTED_MODEL_DIR) 
        
        self.rejected_model = os.path.join(self.model_evaluator_dir, 
                                          REJECTED_MODEL_DIR)
        
        self.evaluation_report = os.path.join(self.model_evaluator_dir,
                                              EVALUATION_REPORT)
        

# if __name__ =="__main__":
#     a = RootConfig()
#     obj = DataIngestionConfig(a)
#     print(obj.__dict__)