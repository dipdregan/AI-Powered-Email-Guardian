import os
from pathlib import Path
from src.utils import read_yaml_file

ROOT_DIR:Path = os.getcwd()
ARTIFACT_DIR:str = "Artifact"

CONFIG_DIR_NAME:str = 'config'
CONFIG_FILE_NAME:str = 'config.yaml'

CONFIG_FILE_PATH:Path = os.path.join(ROOT_DIR, CONFIG_DIR_NAME, CONFIG_FILE_NAME)

CONFIG_FILE = read_yaml_file(CONFIG_FILE_PATH)

# Data Ingestion Related Constants
Data_API: str = CONFIG_FILE['Data_Api']
# Zip_File_Name: str = "ct-kidney-dataset-normal-cyst-tumor-and-stone.zip"
DATA_INGETION_DIR_NAME: str = "data_ingetion"
DATA_INGETION_KAGGLE_DATA_STORE_DIR: str = "zip_file"
DATA_INGETION_UNZIP_DATA_STORE_DIR: str = "unzip_data"
print(Data_API)
