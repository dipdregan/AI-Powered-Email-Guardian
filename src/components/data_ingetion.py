from src.constant.constants import *
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

from src.logger import logging
from src.exception import ham_spam

from pathlib import Path

import zipfile
import os, sys
import subprocess

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ham_spam(e,sys) from e
    
    def importing_data_from_kaggle(self) -> Path:
        try:
            output_dir = os.path.abspath(self.data_ingestion_config.kaggle_data_zip_file_path) # Use the unzip directory as the output directory
            os.makedirs(output_dir, exist_ok=True)

            download_command = self.data_ingestion_config.data_api
            try:
                subprocess.run(download_command, shell=True, check=True, cwd=output_dir)  # Set the current working directory
                print("Dataset downloaded successfully!")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")

            return output_dir
        except Exception as e:
            raise ham_spam(e, sys) from e
            
    def unziping_the_data(self):
        try:
            unzip_dir = self.data_ingestion_config.unzip_file_path
            os.makedirs(unzip_dir, exist_ok=True)
            
            zip_file_dir = self.importing_data_from_kaggle()
            zip_file_name = os.listdir(zip_file_dir)[0]
            zip_file_path = os.path.join(zip_file_dir, zip_file_name)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
                print(f"Data successfully extracted to {unzip_dir}")
            return unzip_dir
        except Exception as e:
            raise ham_spam(e, sys) from e
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info(f"{30*'===='}")
            logging.info(f"{10*'=='}Data Ingestion Started...{10*'=='}")
            logging.info(f"{30*'===='}")
            
            logging.info(f"Data is Downloading from Kaggle...")
            logging.info(f"Storing the data in this folder :{self.data_ingestion_config.kaggle_data_zip_file_path}")
            zip_file_path = self.importing_data_from_kaggle()
            logging.info(f"Data stored in this path {zip_file_path}")
            logging.info(f"{20*'=='}")

            logging.info(f"Unzip the data in to{self.data_ingestion_config.unzip_file_path} ")
            unzip_file_path = self.unziping_the_data()
            logging.info(f"data stored in {unzip_file_path}")
            logging.info(f"{30*'===='}")
            logging.info(f"{10*'=='}Data Ingestion Completed...{10*'=='}")
            logging.info(f"{30*'===='}")

            data_ingestion_artifact = DataIngestionArtifact(
                unzip_data_file_path=unzip_file_path,
                zip_data_file_path=zip_file_path
            )
            print(data_ingestion_artifact)
            return data_ingestion_artifact
        except Exception as e:
            raise ham_spam(e, sys) from e
