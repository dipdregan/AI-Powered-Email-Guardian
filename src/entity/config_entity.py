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

        self.kaggle_data_zip_file_path: str = os.path.join(self.data_ingestion_dir,
                                                           DATA_INGETION_KAGGLE_DATA_STORE_DIR)

        self.unzip_file_path: str = os.path.join(self.data_ingestion_dir,
                                                 DATA_INGETION_UNZIP_DATA_STORE_DIR)

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
                                                                DATA_VALIDATION_INVALID_FILE_NAME)
        self.invalide_data_file_name:str = DATA_VALIDATION_INVALID_FILE_NAME
        
        self.data_validation_report_path:str = os.path.join(self.data_validation_dir,
                                                       DATA_VALIDATION_REPORT_FILE_PATH)
        self.report_file_name:str = DATA_VALIDATION_REPORT_FILE_NAME

class DataTransformationConfig:
    def __init__(self, root_dir:RootConfig):
        self.data_transformation_dir:str = os.path.join(root_dir.artifact_dir,
                                                        DATA_TRANSFORMATION_DIR_NAME)
        
        self.data_transformation_file_name:str = DATA_TRANSFORMATION_FILE_NAME
        

# if __name__ =="__main__":
#     a = RootConfig()
#     obj = DataIngestionConfig(a)
#     print(obj.__dict__)