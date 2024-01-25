from src.components.data_ingetion import DataIngestion

from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.config_entity import DataIngestionConfig,RootConfig
from src.logger import logging
from src.exception import ham_spam
import os, sys

class data_ingestion_Pipeline:
    def __init__(self):
        try:
            self.root_dir = RootConfig()
            
        except Exception as e:
            raise ham_spam(e, sys)
    
    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataIngestionConfig(self.root_dir)
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise e