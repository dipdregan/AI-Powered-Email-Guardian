from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluator
from src.entity.artifact_entity import *
from src.entity.config_entity import *
from constant.constants import *
import os
from src.logger import logging

artifact_paths = {
    "train_file_path": r"artifact\01_30_2024_03_27_18\data_transformation\train_test_data\train.csv",
    "test_file_path": r"artifact\01_30_2024_03_27_18\data_transformation\train_test_data\test.csv"
}

model_trainer_artifact =ModelTrainerArtifact(model_file_path='artifact\\01_30_2024_03_32_05\\model_trainer\\model\\model.h5', training_report_file_path='artifact\\01_30_2024_03_32_05\\model_trainer\\training_report\\training_history.json')
# print(model_trainer_artifact.model_file_path)
data_transformation_artifact = DataTransformationArtifact(**artifact_paths)
config =  ModelEvaluatorConfig(root_dir=RootConfig())
# print(config.__dict__)
obj = ModelEvaluator(config,
               model_trainer_artifact,
               data_transformation_artifact)
obj.initiate_model_evaluation()




# config = ModelTrainerConfig(
#     root_dir=RootConfig()
# )
# logging.info(config.__dict__)
# data_transformation_artifact = DataTransformationArtifact(**artifact_paths)
# # print(data_transformation_artifact.test_file_path)
# # print(data_transformation_artifact.train_file_path)
# obj = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
#                    model_trainer_config=config)
# obj.initiate_model_trainer()