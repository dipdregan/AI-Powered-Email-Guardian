from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_trasnformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.artifact_entity import *
from src.entity.config_entity import *
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
    
    def start_data_validation(self,data_ingestion_artifact):
        try:
            data_validation_config = DataValidationConfig(self.root_dir)
            data_ingestion = DataValidation(data_validation_config,
                                            data_ingestion_artifact)
            
            data_validation_artifact = data_ingestion.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise e
    
    def start_data_transformation(self,data_validation_artifact):
        try:
            data_transformation_config = DataTransformationConfig(self.root_dir)
            data_transformation = DataTransformation(data_transformation_config,
                                                     data_validation_artifact)
            
            data_transformation_artifact= data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise e
    
    def start_model_trainer(self,data_transformation_artifact):
        try:
            model_trainer_config = ModelTrainerConfig(self.root_dir)
            model_tranier = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=model_trainer_config)
            
            model_tranier_artifact= model_tranier.initiate_model_trainer()
            return model_tranier_artifact
        except Exception as e:
            raise e
    
    def initiate_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            # data_validation_artifact = r"artifact\01_25_2024_15_11_32\data_validation\invalid\invalidated_data.csv"
            
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainig_artifact = self.start_model_trainer(data_transformation_artifact)


            # return {'Data Ingress':data_ingestion_artifact,'Data Validation':data_validation_artifact,\
            #        'Model Training':model_trainig_artifact}
            
        except Exception as e:
            raise e