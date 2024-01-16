from src.constant.constants import *
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.logger import logging
from src.exception import ham_spam
import os, sys
import pandas as pd
from src.utils import read_json,write_json

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            # self.data_ingestion_artifact = data_ingestion_artifact
            # self.data_file_dir = data_ingestion_artifact.unzip_data_file_path
        except Exception as e:
            raise ham_spam(e, sys) from e

    def _read_data(self, file_path: str) -> pd.DataFrame:
        """Read data from a file."""
        logging.info(f"Reading data from: {file_path}")
        return pd.read_csv(file_path, sep='\t', names=[TARGET_NAME, FEATURES_NAME])

    def _validate_data(self, df: pd.DataFrame, data_types: dict) -> bool:
        """Validate the input data."""
        logging.info("Validating data...")
        # Implement your data validation logic here

        # Example: Check if required columns are present
        if FEATURES_NAME not in df.columns or TARGET_NAME not in df.columns:
            raise ham_spam("Missing required columns in the input data.")

        # Validate data types
        for column, expected_type in data_types.items():
            if column not in df.columns:
                raise ham_spam(f"Column '{column}' is missing in the input data.")
            actual_type = df[column].dtype
            if actual_type != expected_type:
                raise ham_spam(f"Data type mismatch for column '{column}'. Expected '{expected_type}', got '{actual_type}'.")

        logging.info("Data validation completed successfully.")
        return True

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

    def _save_validation_report(self, report: dict, report_file_path: str) -> None:
        """Save validation report to a JSON file."""
        write_json(report, report_file_path)
        logging.info(f"Validation report saved to: {report_file_path}")

    def initiate_data_validation(self,artifact) -> DataValidationArtifact:
        try:
            logging.info(f"{30*'===='}")
            logging.info(f"{10*'=='}Data Validation Started...{10*'=='}")
            logging.info(f"{30*'===='}")

            # Read data
            # data_dir = artifact.unzip_data_file_path
            data_dir = artifact
            file_name = os.listdir(data_dir)[0]
            file_path = os.path.join(data_dir, file_name)
            df = self._read_data(file_path)
            logging.info(f"Data :\n {df.head()}")
        
            # Read data types from configuration file
            data_types_config = read_yaml_file(CONFIG_FILE_PATH)['columns_data_type']
            data_types = {item: data_type for item, data_type in data_types_config.items()}

            # Validate data
            self._validate_data(df, data_types)
            os.makedirs(self.data_validation_config.data_validation_validate_path, exist_ok= True)
            validated_data_path = os.path.join(self.data_validation_config.data_validation_validate_path,
                                               self.data_validation_config.valide_data_file_name)
            # Save validated and invalidated data

            self._save_data(df, validated_data_path)

        #     # You can save invalidated data as well based on your validation logic

            # Generate and save validation report
            validation_report = self._generate_validation_report(validation_result=True)
            os.makedirs(self.data_validation_config.data_validation_report_path, exist_ok= True)
            report_file_path = os.path.join(self.data_validation_config.data_validation_report_path,
                                self.data_validation_config.report_file_name)
            self._save_validation_report(validation_report, report_file_path)


            data_validation_artifact = DataValidationArtifact(
                validated_data_path=validated_data_path,
                invalidated_data_path=None,
                validation_report_path=report_file_path
            )

            logging.info(f"{30*'===='}")
            logging.info(f"{10*'=='}Data Validation Completed...{10*'=='}")
            logging.info(f"{30*'===='}")

            return data_validation_artifact

        except FileNotFoundError as e:
            error_message = f"File not found: {e}"
            logging.error(error_message)
            validation_report = self._generate_validation_report(validation_result=False, error_message=error_message)
            report_file_path = os.path.join(self.data_validation_config.data_validation_report_path,
                                            self.data_validation_config.report_file_name)
            self._save_validation_report(validation_report, report_file_path)
            raise ham_spam("Error occurred during data validation. File not found.") from e

        except pd.errors.EmptyDataError as e:
            error_message = f"Empty data file: {e}"
            logging.error(error_message)
            validation_report = self._generate_validation_report(validation_result=False, error_message=error_message)
            report_file_path = os.path.join(self.data_validation_config.data_validation_report_path,
                                            self.data_validation_config.report_file_name)
            self._save_validation_report(validation_report, report_file_path)
            raise ham_spam("Error occurred during data validation. Empty data file.") from e

        except Exception as e:
            error_message = f"Unexpected error: {e}"
            logging.error(error_message)
            validation_report = self._generate_validation_report(validation_result=False, error_message=error_message)
            report_file_path = os.path.join(self.data_validation_config.data_validation_report_path,
                                            self.data_validation_config.report_file_name)
            self._save_validation_report(validation_report, report_file_path)
            raise ham_spam("Error occurred during data validation.") from e