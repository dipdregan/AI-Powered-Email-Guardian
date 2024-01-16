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
        self.data_ingestion_dir: str = os.path.join(root_dir.artifact_dir, DATA_INGETION_DIR_NAME)

        self.kaggle_data_zip_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGETION_KAGGLE_DATA_STORE_DIR)

        self.unzip_file_path: str = os.path.join(self.data_ingestion_dir, DATA_INGETION_UNZIP_DATA_STORE_DIR)

        self.data_api: str = Data_API

# if __name__ =="__main__":
#     a = RootConfig()
#     obj = DataIngestionConfig(a)
#     print(obj.__dict__)