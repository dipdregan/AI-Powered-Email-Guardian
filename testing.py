from components.data_ingetion import DataIngestion
from entity.config_entity import DataIngestionConfig,RootConfig,DataTransformationConfig

from components.data_validation import DataValidation
from entity.config_entity import *
from components.data_trasnformation import DataTransformation
from entity.artifact_entity import *
from src.components.model_trainer import ModelTrainer
from src.logger import logging

config = ModelTrainerConfig(
    root_dir=RootConfig()
)
logging.info(config.__dict__)
artifact_paths = {
    "train_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/train.csv",
    "test_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/test.csv"
}

data_transformation_artifact = DataTransformationArtifact(**artifact_paths)
# print(data_transformation_artifact.test_file_path)
# print(data_transformation_artifact.train_file_path)
obj = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                   model_trainer_config=config)
obj.initiate_model_trainer()


# config = DataTransformationConfig(
#     root_dir=RootConfig()
# )

# # print(config.__dict__)
# data_ingestion_artifact = r"F:\End_To_End_project\Ham_Spam_Classifier(ETE)\artifact\01_25_2024_15_18_34\data_validation\invalid\invalidated_data.csv"
# obj = DataTransformation(config,data_ingestion_artifact)
# obj.initiate_data_transformation()




##### ============================ Data Ingestion Testing Completed ================================

# config = DataIngestionConfig(
#     root_dir=RootConfig()
# )
# # print(config.__dict__)
# obj = DataIngestion(data_ingestion_config=config)
# obj.initiate_data_ingestion()