from src.components.model_pusher import ModelLoader
from src.entity.artifact_entity import *

data = DataTransformationArtifact(data_transformation_path='artifact\\02_12_2024_02_12_46\\data_transformation\\transform_data\\transform_data.csv', feature_data_file_path='artifact\\02_12_2024_02_12_46\\data_transformation\\feature_target_data\\Text_pad_sequences.npy', label_data_file_path='artifact\\02_12_2024_02_12_46\\data_transformation\\feature_target_data\\label.npy', preprocess_file_path='artifact\\02_12_2024_02_12_46\\data_transformation\\preprocess_file')
model= ModelEvaluatorArtifact(accepted_model_path='artifact\\02_12_2024_02_12_46\\model_evaluator\\accepted_model\\combined.h5', evaluation_report_path='artifact\\02_12_2024_02_12_46\\model_evaluator\\evaluation_report')

obj = ModelLoader(data,model)
print(obj.accessing_path_s3())
print(obj.uploading_process_pkl())