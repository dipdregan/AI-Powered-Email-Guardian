from dataclasses import dataclass
from typing import List
from pathlib import Path

@dataclass
class DataIngestionArtifact:
    zip_data_file_path:Path
    unzip_data_file_path:Path
