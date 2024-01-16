from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    zip_data_file_path:Path
    unzip_data_file_path:Path

@dataclass
class DataValidationArtifact:
    validated_data_path:Path
    invalidated_data_path:Path
    validation_report_path:Path

@dataclass
class DataTransformationArtifact:
    data_transformation_path:Path
