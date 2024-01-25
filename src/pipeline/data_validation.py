from src.components.data_validation import DataValidation

from src.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from src.entity.config_entity import DataValidationConfig,RootConfig
from src.logger import logging
from src.exception import ham_spam
import os, sys

class data_validation_Pipeline:
    def __init__(self):
        try:
            self.root_dir = RootConfig()
            
        except Exception as e:
            raise ham_spam(e, sys)

    def start_data_validation(self,data_ingestion_artifact):
        try:
            data_validation_config = DataValidationConfig(self.root_dir)
            data_validation = DataValidation(data_validation_config,
                                             data_ingestion_artifact)
            data_validation_artifact= data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise e