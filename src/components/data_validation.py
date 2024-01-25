from src.constant.constants import *
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.logger import logging
from src.exception import ham_spam
import os, sys
import pandas as pd
from src.utils import read_json, write_json
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

        expected_columns = read_yaml_file(CONFIG_FILE_PATH)['columns_data_type']
        logging.info(expected_columns)
        is_valid_columns = set(df.columns) == set(self.expected_columns)
        logging.info(set(df.columns),set(self.expected_columns))
        if not is_valid_columns:
            print("Column name validation failed. Unexpected columns found.")

        # # Data type validation
        # is_valid_data_types = True
        # for column, expected_dtype in self.data_types.items():
        #     actual_dtype = df[column].dtype
        #     if actual_dtype != expected_dtype:
        #         print(f"Data type validation failed for column '{column}': Expected {expected_dtype}, but got {actual_dtype}")
        #         is_valid_data_types = False

        return is_valid_columns 
    # and is_valid_data_types

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

        # data_dir = self.data_ingestion_artifact.unzip_data_file_path
        data_dir = self.data_ingestion_artifact
        file_name = os.listdir(data_dir)[0]
        file_path = os.path.join(data_dir, file_name)
        # print(file_path)
        df = self._read_data(file_path)
        logging.info(f"\n:{df.head()}")

        validation_rules_config = read_yaml_file(CONFIG_FILE_PATH)['columns_data_type']
        validation_dtype = {column: dtype for column, dtype in validation_rules_config.items()}
        logging.info(validation_dtype)
        self.validate_dataframe_with_config(df)
        # Validating data and handle invalidated data
        # invalidated_data, validated_data = 
        # logging.info(invalidated_data)
        # logging.info(validated_data)
        # if not validated_data.empty:
        #     # Save validated data
        #     os.makedirs(Config.data_validation_validate_path,exist_ok=True)
        #     validated_data_path = os.path.join(Config.data_validation_dir,
        #                                        Config.valide_data_file_name)
        #     logging.info(f"Validated data saved to: {validated_data_path}")
        # else:
        #     logging.info("No validated data to save.")
        # if not invalidated_data.empty:
        #     os.makedirs(Config.data_validation_invalidate_path,exist_ok=True)
        #     invalidated_data_path = os.path.join(
        #         Config.data_validation_invalidate_path,
        #         Config.invalide_data_file_name
        #     )
        #     self._save_data(df = invalidated_data,save_path=invalidated_data_path)
        #     logging.info(f"Invalidated data saved to: {invalidated_data_path}")
        # else:
        #     logging.info("No invalidated data to save.")

        #     # Generate and save validation report
        #     validation_report = self._generate_validation_report(validation_result=True)
        #     write_json(validation_report, report_file_path)
        #     logging.info(f"Validation report saved to: {report_file_path}")


        #     data_validation_artifact = DataValidationArtifact(
        #         validated_data_path=validated_data_path if not validated_data.empty else None,
        #         invalidated_data_path=invalidated_data_path if not invalidated_data.empty else None,
        #         validation_report_path=report_file_path
        #     )

        #     logging.info(f"{30 * '===='}")
        #     logging.info(f"{10 * '=='}Data Validation Completed...{10 * '=='}")
        #     logging.info(f"{30 * '===='}")

        #     return data_validation_artifact

        # # # except Exception as e:
        # # #     validation_result = False
        # # #     exc_info = sys.exc_info()

        # # #     # Handle KeyError specifically
        # # #     if isinstance(e, KeyError):
        # # #         error_message = f"KeyError occurred: {str(e)}"
        # # #     else:
        # # #         error_message = str(e)

        # # #     # Generate and save validation report with error message
        # # #     validation_report = self._generate_validation_report(validation_result=validation_result, error_message=error_message)
        # # #     write_json(validation_report, report_file_path)
        # # #     logging.info(f"Validation report saved to: {report_file_path}")

        # # #     raise ham_spam(error_message, sys) from e

