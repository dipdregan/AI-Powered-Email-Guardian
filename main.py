from src.utils import read_yaml_file
from src.constant import constants
from src.entity.config_entity import DataIngestionConfig,RootConfig
from src.logger import logging
# from src.components.data_ingetion import DataIngestion
from src.components.data_ingetion import DataIngestion
root_dir = RootConfig()
config = DataIngestionConfig(root_dir=root_dir)
obj = DataIngestion(config)
obj.initiate_data_ingestion()


# if __name__ == "__main__":
#     config = DataIngetionConfig(root_dir=root_config)
#     data_ingestion = DataIngestion(config)
#     data_ingestion.initiate_data_ingestion()

# if __name__=="__main__":
#     root_dir = RootConfig()
#     obj = DataIngestionConfig(root_dir=root_dir)
#     print(obj.__dict__)
#     logging.info(obj.__dict__)