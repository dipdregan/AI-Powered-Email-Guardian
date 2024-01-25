from components.data_ingetion import DataIngestion
from entity.config_entity import DataIngestionConfig,RootConfig

from components.data_validation import DataValidation
from entity.config_entity import DataValidationConfig,DataTransformationConfig
from components.data_trasnformation import DataTransformation
# from entity.artifact_entity import DataIngestionArtifact



##### ============================ Data tranformation Testing Completed ================================
config = DataTransformationConfig(RootConfig())
data_val_artifact = r"D:\Projects_NLP\Ham_Spam_Classifier-ETE-\artifact\01_25_2024_23_53_17\data_validation\validated\validated_data.csv"
obj = DataTransformation(config,data_val_artifact)
obj.initiate_data_transformation()




##### ============================ Data validation Testing Completed ================================



# config = DataValidationConfig(
#     root_dir=RootConfig()
# )
# # print(config.__dict__)
# data_ingestion_artifact = r"D:\Projects_NLP\Ham_Spam_Classifier-ETE-\artifact\01_25_2024_23_50_00\data_ingetion\unzip_data"
# obj = DataValidation(data_validation_config=config,
#                      data_ingestion_artifact=data_ingestion_artifact)
# obj.initiate_data_validation()




#### ============================ Data Ingestion Testing Completed ================================

# config = DataIngestionConfig(
#     root_dir=RootConfig()
# )
# # print(config.__dict__)
# obj = DataIngestion(data_ingestion_config=config)
# obj.initiate_data_ingestion()