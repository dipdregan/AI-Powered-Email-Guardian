from src.components.data_ingetion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_trasnformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluator
from src.components.model_pusher import ModelLoader

from src.entity.artifact_entity import *
from src.entity.config_entity import *
from src.logger import logging
from src.exception import ham_spam

import os
import sys
import subprocess

class Pipeline:
    def __init__(self):
        try:
            self.root_dir = RootConfig()
        except Exception as e:
            raise ham_spam(e, sys)

    def start_data_ingestion(self, **kwargs):
        try:
            data_ingestion_config = DataIngestionConfig(self.root_dir)
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion(**kwargs)
            return data_ingestion_artifact
        except Exception as e:
            raise e

    def start_data_validation(self, data_ingestion_artifact, **kwargs):
        try:
            data_validation_config = DataValidationConfig(self.root_dir)
            data_validation = DataValidation(data_validation_config, data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation(**kwargs)
            return data_validation_artifact
        except Exception as e:
            raise e

    def start_data_transformation(self, data_validation_artifact, **kwargs):
        try:
            data_transformation_config = DataTransformationConfig(self.root_dir)
            data_transformation = DataTransformation(data_transformation_config, data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation(**kwargs)
            return data_transformation_artifact
        except Exception as e:
            raise e

    def start_model_trainer(self, data_transformation_artifact, **kwargs):
        try:
            model_trainer_config = ModelTrainerConfig(self.root_dir)
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer(**kwargs)
            return model_trainer_artifact
        except Exception as e:
            raise e
        
    def start_model_evaluation(self, data_transformation_artifact, model_trainer_artifact):
        try:
            model_evaluation_config = ModelEvaluatorConfig(self.root_dir)
            model_evaluation = ModelEvaluator(data_transformation_artifact=data_transformation_artifact,
                                               model_trainer_artifacts=model_trainer_artifact,
                                               model_evaluation_config=model_evaluation_config)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise e
        
    def start_model_pusher(self, data_transformation_artifact, model_evaluation_artifact):
        try:
            model_loader = ModelLoader(data_transformation_artifact,
                                        model_evaluation_artifact)
            model_loader_artifact = model_loader.initiate_model_pusher()
            return model_loader_artifact
        except Exception as e:
            raise e


    def initiate_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_training_artifact = self.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_transformation_artifact,
                                                                     model_training_artifact)
            model_pusher_artifact = self.start_model_pusher(data_transformation_artifact,
                                                             model_evaluation_artifact)

            return {
                'Data Ingestion': data_ingestion_artifact,
                'Data Validation': data_validation_artifact,
                'Data Transformation': data_transformation_artifact,
                'Model Training': model_training_artifact,
                'Model Evaluation': model_evaluation_artifact,
                'Model Pusher': model_pusher_artifact
            }
        except Exception as e:
            raise e




# from src.components.data_ingetion import DataIngestion
# from src.components.data_validation import DataValidation
# from src.components.data_trasnformation import DataTransformation
# from src.components.model_trainer import ModelTrainer

# from src.entity.artifact_entity import *
# from src.entity.config_entity import *
# from src.logger import logging
# from src.exception import ham_spam

# from exception import ham_spam
# import os, sys

# class Pipeline:
#     def __init__(self):
#         try:
#             self.root_dir = RootConfig()
            
#         except Exception as e:
#             raise ham_spam(e, sys)
    
#     def start_data_ingestion(self):
#         try:
#             data_ingestion_config = DataIngestionConfig(self.root_dir)
#             data_ingestion = DataIngestion(data_ingestion_config)
#             data_ingestion_artifact= data_ingestion.initiate_data_ingestion()

#             return data_ingestion_artifact
#         except Exception as e:
#             raise e
    
#     def start_data_validation(self, data_ingestion_artifact):
#         try:
#             data_validation_config = DataValidationConfig(self.root_dir)
#             data_ingestion = DataValidation(data_validation_config, data_ingestion_artifact)
            
#             data_validation_artifact = data_ingestion.initiate_data_validation()
#             return data_validation_artifact
#         except Exception as e:
#             raise e
    
#     def start_data_transformation(self, data_validation_artifact):
#         try:
#             data_transformation_config = DataTransformationConfig(self.root_dir)
#             data_transformation = DataTransformation(data_transformation_config, data_validation_artifact)
            
#             data_transformation_artifact = data_transformation.initiate_data_transformation()
#             return data_transformation_artifact
#         except Exception as e:
#             raise e
    
#     def start_model_trainer(self, data_transformation_artifact):
#         try:
#             model_trainer_config = ModelTrainerConfig(self.root_dir)
#             model_tranier = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
#                                          model_trainer_config=model_trainer_config)
            
#             model_tranier_artifact = model_tranier.initiate_model_trainer()
#             return model_tranier_artifact
#         except Exception as e:
#             raise e
    
#     def initiate_pipeline(self):
#         try:
#             data_ingestion_artifact = self.start_data_ingestion()
#             data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
#             data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
#             model_training_artifact = self.start_model_trainer(data_transformation_artifact)

#             return {
#                 'Data Ingestion': data_ingestion_artifact,
#                 'Data Validation': data_validation_artifact,
#                 'Data Transformation': data_transformation_artifact,
#                 'Model Training': model_training_artifact
#             }
            
#         except Exception as e:
#             raise e

# if __name__ == "__main__":
#     pipeline = Pipeline()
#     artifacts = pipeline.initiate_pipeline()
#     print("Artifacts produced:", artifacts)
