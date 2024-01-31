import os
from src.entity.artifact_entity import DataTransformationArtifact
from src.entity.config_entity import ModelTrainerConfig,RootConfig
from src.components.model_trainer import ModelTrainer

# Replace these paths with the actual paths of your artifacts
data_transformation_path = 'artifact\\01_31_2024_03_35_23\\data_transformation\\transform_data\\transform_data.csv'
feature_data_path = 'artifact\\01_31_2024_03_35_23\\data_transformation\\feature_target_data\\Text_pad_sequences.npy'
label_data_path = 'artifact\\01_31_2024_03_35_23\\data_transformation\\feature_target_data\\label.npy'
preprocess_file_path = 'artifact\\01_31_2024_03_35_23\\data_transformation\\preprocess_file'

# Create DataTransformationArtifact
data_transformation_artifact = DataTransformationArtifact(
    data_transformation_path=data_transformation_path,
    feature_data_file_path=feature_data_path,
    label_data_file_path=label_data_path,
    preprocess_file_path=preprocess_file_path
)

# Create ModelTrainerConfig
model_trainer_config = ModelTrainerConfig(root_dir=RootConfig())  # You need to provide the actual configuration

# Create ModelTrainer
model_trainer = ModelTrainer(data_transformation_artifact, model_trainer_config)

print(model_trainer.X)
# Run the pipeline for multiple model types
 # Add or remove model types based on your requirements
# artifacts = model_trainer.initiate_model_trainer()


