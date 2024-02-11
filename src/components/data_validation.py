from src.constant.constants import *
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.logger import logging
from src.exception import ham_spam
import os, sys
import pandas as pd
from src.utils.utils import read_json, write_json
from typing import Tuple

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_types = data_validation_config.data_types
            self.expected_columns = data_validation_config.expected_columns
        except Exception as e:
            raise ham_spam(e, sys) from e

    def _read_data(self, file_path: str) -> pd.DataFrame:
        """Read data from a file."""
        try:
            logging.info(f"Reading data from: {file_path}")
            df = pd.read_csv(file_path, encoding='latin1')
            logging.info("Finding out the Null features.......>>")
            logging.info(f"Null Features name:\n{df.isna().sum()}")

            logging.info("Dropping the Null features.......>>")
            df = df.dropna(axis=1, inplace=False)
            df = df.rename(columns={'v1': TARGET_NAME, 'v2': FEATURES_NAME}, inplace=False)

            return df
        except Exception as e:
            raise ham_spam(e)

    
    def validate_dataframe_with_config(self,df):
        try:
            is_valid_columns = set(df.columns) == set(self.expected_columns)
            
            error_message = ''
            if not is_valid_columns:
                error_message = f"Column name validation failed. Unexpected columns found."
                logging.info("Column name validation failed. Unexpected columns found.")

            else :
                logging.info(f"<<<<<<<<<<<=========   Column name validation succesfully completed   ======>>>>>>>")
                is_valid_data_types = True
                for column, dtype in self.data_types.items():
                    actual_dtype = df[column].dtype
                    if actual_dtype != dtype:
                        logging.info(f"Data type validation failed for column '{column}'==> Expected: {actual_dtype}, but got :{dtype} ")
                        error_message = f"Data type validation failed for column '{column}'==> Expected: {actual_dtype}, but got :{dtype} "
                        is_valid_data_types = False
                        
            return is_valid_data_types,error_message
        
        except Exception as e:
            raise ham_spam(sys,e) from e
 

    def _save_data(self, df: pd.DataFrame, save_path: str) -> None:
        """Save data to a file."""
        df.to_csv(save_path, index=False)
        logging.info(f"Data saved to: {save_path}")

    def _generate_validation_report(self, validation_result: bool, error_message: str = "") -> dict:
        """Generate a validation report."""
        report = {
            "validation_result": validation_result,
            "error_message": error_message,
        }
        return report

    def initiate_data_validation(self) -> DataValidationArtifact:
        Config = self.data_validation_config
        os.makedirs(Config.data_validation_report_path, exist_ok=True)
        report_file_path = os.path.join(Config.data_validation_report_path,
                                        Config.report_file_name)
        # try:
        logging.info(f"{30 * '===='}")
        logging.info(f"{10 * '=='}Data Validation Started...{10 * '=='}")
        logging.info(f"{30 * '===='}")

        data_dir = self.data_ingestion_artifact.unzip_data_file_path
        # data_dir = self.data_ingestion_artifact
        file_name = os.listdir(data_dir)[0]
        file_path = os.path.join(data_dir, file_name)
        # print(file_path)
        df = self._read_data(file_path)
        logging.info(f"\n:{df.head()}")

        data_validation ,error = self.validate_dataframe_with_config(df)

        if data_validation:
            os.makedirs(Config.data_validation_validate_path,exist_ok=True)
            validated_data_path = os.path.join(Config.data_validation_validate_path,
                                               Config.valide_data_file_name)
            self._save_data(df,validated_data_path)
            logging.info(f"Validated data saved to: {validated_data_path}")

        else:
            os.makedirs(Config.data_validation_invalidate_path,exist_ok=True)
            invalidated_data_path = os.path.join(Config.data_validation_invalidate_path,
                                               Config.invalide_data_file_name)
            self._save_data(df,invalidated_data_path)
            logging.info(f"Validated data saved to: {invalidated_data_path}")

        # Generate and save validation report
        validation_report = self._generate_validation_report(validation_result=data_validation ,
                                                             error_message=error)
        write_json(validation_report, report_file_path)
        logging.info(f"Validation report saved to: {report_file_path}")

        
        data_validation_artifact = DataValidationArtifact(
            validated_data_path=validated_data_path if data_validation else None,
            invalidated_data_path=invalidated_data_path if not data_validation else None,
            validation_report_path=report_file_path
        )

        logging.info(f"{30 * '===='}")
        logging.info(f"{10 * '=='}Data Validation Completed...{10 * '=='}")
        logging.info(f"{30 * '===='}")
        logging.info(data_validation_artifact)

        return data_validation_artifact

