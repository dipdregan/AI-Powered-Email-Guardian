from components.data_ingetion import DataIngestion
from entity.config_entity import DataIngestionConfig,RootConfig

from components.data_validation import DataValidation
from entity.config_entity import DataValidationConfig
# from entity.artifact_entity import DataIngestionArtifact


config = DataValidationConfig(
    root_dir=RootConfig()
)
# print(config.__dict__)
data_ingestion_artifact = r"F:\End_To_End_project\Ham_Spam_Classifier(ETE)\artifact\01_23_2024_22_49_03\data_ingetion\unzip_data"
obj = DataValidation(data_validation_config=config,
                     data_ingestion_artifact=data_ingestion_artifact)
obj.initiate_data_validation()



######


##### ============================ Data Ingestion Testing Completed ================================

# config = DataIngestionConfig(
#     root_dir=RootConfig()
# )
# # print(config.__dict__)
# obj = DataIngestion(data_ingestion_config=config)
# obj.initiate_data_ingestion()
