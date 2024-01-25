from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
# from src.components.data_trasnformation import DataTransformation

from src.entity.artifact_entity import *
from src.entity.config_entity import *
from src.logger import logging
from src.exception import ham_spam
import os, sys

class TRAINING_PIPELINE:
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
    def start_data_validation(self,data_ingestion_artifact):
        try:
            data_validation_config = DataIngestionConfig(self.root_dir)
            data_validation = DataValidation(data_validation_config)
            data_validation_artifact= data_validation.initiate_data_ingestion()
            return data_validation_artifact
        except Exception as e:
            raise e
        
    # def start_data_transformation(self,data_validation_artifacts):
    #     try:
    #         data_transformation_config = DataTransformationConfig(self.root_dir)
    #         data_transfomation = DataTransformation(data_transformation_config)
    #         data_transfomation_artifact= data_transfomation.initiate_data_ingestion()
    #         return data_transfomation_artifact
    #     except Exception as e:
    #         raise e
        
    def run_pipeline(self):
        try:
            # data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_ingestion_artifact = Path(r"artifact\01_16_2024_14_06_15\data_ingetion\unzip_data")

            data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            # # data_validation_artifact = r"F:\End_To_End_project\Kidney_Disease_Classification_DL\artifact\11_10_2023_09_04_08\Image_Data_Validation"

            # data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
        
        except Exception as e:
            raise e