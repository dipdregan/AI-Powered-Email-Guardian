from src.entity.config_entity import *
from src.entity.artifact_entity import *
from src.components.data_ingetion import DataIngestion
from src.components.data_validation import *
from src.components.data_trasnformation import *

if __name__=="__main__":
    config = DataValidationConfig(RootConfig())
    data_ingestion_artifact = r"artifact\01_17_2024_18_42_01\data_ingetion\unzip_data"
    obj = DataValidation(config,data_ingestion_artifact)
    obj.initiate_data_validation()
# if __name__=="__main__":
#     config = DataIngestionConfig(RootConfig())
#     DataIngestion(config).initiate_data_ingestion()


# if __name__ == "__main__":
#     config = DataValidationConfig(RootConfig())
#     path =  Path(r"artifact\01_17_2024_07_36_15\data_ingetion\unzip_data")
#     obj = DataValidation(config,path)
#     obj.initiate_data_validation()
    # DataValidationArtifact = Path(r"artifact\01_17_2024_07_36_15\data_ingetion\unzip_data")
    # config = DataTransformationConfig(RootConfig())
    # obj = DataTransformation(config,DataValidationArtifact)
    # obj.initiate_data_transformation()

# root_dir = RootConfig()
# config = DataValidationConfig(root_dir=root_dir)
# data_ingestion_artifact = r"artifact\01_16_2024_22_58_39\data_ingetion\unzip_data"
# obj = DataValidation(config,data_ingestion_artifact)
# obj.initiate_data_validation()

# if __name__ == "__main__":
#     root_dir = RootConfig()
#     config = DataIngestionConfig(root_dir=root_dir)
#     DataIngestion(data_ingestion_config=config).initiate_data_ingestion()




























# from src.utils import read_yaml_file
# from src.constant.constants import CONFIG_FILE
# from src.entity.config_entity import *
# from src.entity.artifact_entity import DataValidationArtifact
# from src.logger import logging
# from src.components.data_validation import DataValidation
# from pathlib import Path
# from src.pipeline.data_pipeline import TRAINING_PIPELINE
# from src.components.data_trasnformation import DataTransformation



# DataValidationArtifact = Path(r"artifact\01_16_2024_16_44_27\data_validation\validated\validated_data.csv")
# config = DataTransformationConfig(RootConfig())
# obj = DataTransformation(config,DataValidationArtifact)
# obj.initiate_data_transformation()

# obj = TRAINING_PIPELINE()
# run = obj.run_pipeline()
# print(obj)


# data_ingestion_artifact = Path(r"artifact\01_16_2024_14_06_15\data_ingetion\unzip_data")
# root_dir=RootConfig()
# obj = DataValidationConfig(root_dir=root_dir)
# obj1 = DataValidation(obj,data_ingestion_artifact)
# obj1.initiate_data_validation(data_ingestion_artifact)


# from src.components.data_ingetion import DataIngestion
# from src.components.data_ingetion import DataIngestion
# root_dir = RootConfig()
# config = DataIngestionConfig(root_dir=root_dir)
# obj = DataIngestion(config)
# # obj.initiate_data_ingestion()
# print(CONFIG_FILE)


# if __name__ == "__main__":
#     config = DataIngetionConfig(root_dir=root_config)
#     data_ingestion = DataIngestion(config)
#     data_ingestion.initiate_data_ingestion()

# if __name__=="__main__":
#     root_dir = RootConfig()
#     obj = DataIngestionConfig(root_dir=root_dir)
#     print(obj.__dict__)
#     logging.info(obj.__dict__)