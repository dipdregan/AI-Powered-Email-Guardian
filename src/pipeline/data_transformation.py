from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_trasnformation import DataTransformation

from src.entity.artifact_entity import *
from src.entity.config_entity import *
from src.logger import logging
from src.exception import ham_spam
import os, sys

class data_transfomation_Pipeline:
    def __init__(self):
        try:
            self.root_dir = RootConfig()
            
        except Exception as e:
            raise ham_spam(e, sys)
        
    def start_data_transformation(self,data_validation_artifacts):
        try:
            data_transformation_config = DataTransformationConfig(self.root_dir)
            data_transfomation = DataIngestion(data_transformation_config)
            data_transfomation_artifact= data_transfomation.initiate_data_ingestion()
            return data_transfomation_artifact
        except Exception as e:
            raise e
        
