import os
from pathlib import Path
from src.utils import read_yaml_file

ROOT_DIR:Path = os.getcwd()
ARTIFACT_DIR:str = "artifact"

CONFIG_DIR_NAME:str = 'config'
CONFIG_FILE_NAME:str = 'config.yaml'
PARAMS_FILE_NAME:str = 'params.yaml'

CONFIG_FILE_PATH:Path = os.path.join(ROOT_DIR, CONFIG_DIR_NAME, CONFIG_FILE_NAME)
PARAMS_FILE_PATH:Path = os.path.join(ROOT_DIR, CONFIG_DIR_NAME, PARAMS_FILE_NAME)

CONFIG_FILE = read_yaml_file(CONFIG_FILE_PATH)
PARAMS_FILE= read_yaml_file(PARAMS_FILE_PATH)
# print(CONFIG_FILE)

# Data Ingestion Related Constants
Data_API: str = CONFIG_FILE['Data_Api']
DATA_INGETION_DIR_NAME: str = "data_ingetion"
DATA_INGETION_KAGGLE_DATA_STORE_DIR: str = "zip_file"
DATA_INGETION_UNZIP_DATA_STORE_DIR: str = "unzip_data"

"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_VALID_FILE_NAME:str ="validated_data.csv"

DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_INVALID_FILE_NAME:str ="invalidated_data.csv"

FEATURES_NAME:str = CONFIG_FILE['columns_name']['feature']
TARGET_NAME:str = CONFIG_FILE['columns_name']['label']

DATA_VALIDATION_REPORT_FILE_PATH:str = "validation_report"
DATA_VALIDATION_REPORT_FILE_NAME:str = "report.json"


"""
Data Transformation realted contant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
TRASNFORM_DATA_DIR_NAME:str = "transform_data"
TRANSFORM_DATA_FILE_NAME:str = "transform_data.csv"
SPLITTED_DATA_DIR:str = "train_test_data"

TEST_SET_SIZE:float=0.2
RANDOM_STATE:int=42
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"


"""
Model_Trainer Related constant
"""
MODEL_TRAINER:str = "model_trainer"
MODEL_DIR:str ="model"
MODEL_NAME:str = PARAMS_FILE['model_name']

TRAINING_HISTORY_DIR:str = "training_report"
TRAINING_HISTORY_FILE_NAME:str = PARAMS_FILE['training_history']

