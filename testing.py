from src.main_pipeline.main_pipeline import Pipeline

Pipeline().initiate_pipeline()

# # from components.data_ingetion import DataIngestion
# from entity.config_entity import DataIngestionConfig,RootConfig,DataTransformationConfig

# # from components.data_validation import DataValidation
# from entity.config_entity import *
# from components.data_trasnformation import DataTransformation
# # from entity.artifact_entity import *
# # from src.components.model_trainer import ModelTrainer
# # from src.components.model_evaluation import ModelEvaluator
# from src.logger import logging

# config = DataTransformationConfig(
#     root_dir=RootConfig()
# )

# # print(config.__dict__)
# data_ingestion_artifact = r"F:\End_To_End_project\Ham_Spam_Classifier(ETE)\artifact\01_25_2024_15_11_32\data_validation\invalid\invalidated_data.csv"
# obj = DataTransformation(config,data_ingestion_artifact)
# obj.initiate_data_transformation()


# def model_trainer():
#     config = ModelTrainerConfig(
#     root_dir=RootConfig()
#     )
#     logging.info(config.__dict__)
#     artifact_paths = {
#         "train_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/train.csv",
#         "test_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/test.csv"
#     }
#     data_transformation_artifact = DataTransformationArtifact(**artifact_paths)
#     obj = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
#                        model_trainer_config=config)
#     model_arfticat,history = obj.initiate_model_trainer()
#     return model_arfticat, history

# def model_evaluation(model_arfticat,history):

#     config = ModelEvaluatorConfig(RootConfig())
#     data_artifact = {
#         "train_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/train.csv",
#         "test_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/test.csv"
#     }

#     data_transformation_artifact = DataTransformationArtifact(**data_artifact)
#     obj = ModelEvaluator(model_evaluation_config=config,
#                 model_trainer_artifact=model_arfticat,
#                 data_transformation_artifact=data_transformation_artifact)
#     obj.initiate_model_evaluation()


# if __name__ == "__main__":

#     model_arfticat, history = model_trainer()
#     model_evaluation(model_arfticat,history)

# ### ======================= Model_ Evaluation Started ==============
# config = ModelEvaluatorConfig(RootConfig())

# model_arfticat = r"F:\End_To_End_project\Ham_Spam_Classifier(ETE)\artifact\01_30_2024_00_16_14\model_trainer\model\model.h5"
# data_artifact = {
#     "train_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/train.csv",
#     "test_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/test.csv"
# }

# data_transformation_artifact = DataTransformationArtifact(**data_artifact)

# # model_arfticat = ModelTrainerArtifact(**model_arfticat)

# # print(data_transformation_artifact)
# # print(model_arfticat)

# obj = ModelEvaluator(model_evaluation_config=config,
#                model_trainer_artifact=model_arfticat,
#                data_transformation_artifact=data_transformation_artifact)
# obj.initiate_model_evaluation()



# ###  =========================== Model Trainer Completed ==================
# # config = ModelTrainerConfig(
# #     root_dir=RootConfig()
# )
# logging.info(config.__dict__)
# artifact_paths = {
#     "train_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/train.csv",
#     "test_file_path": "artifact/01_29_2024_19_16_48/data_transformation/train_test_data/test.csv"
# }

# data_transformation_artifact = DataTransformationArtifact(**artifact_paths)
# # print(data_transformation_artifact.test_file_path)
# # print(data_transformation_artifact.train_file_path)
# obj = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
#                    model_trainer_config=config)
# obj.initiate_model_trainer()







##### ============================ Data Ingestion Testing Completed ================================

# config = DataIngestionConfig(
#     root_dir=RootConfig()
# )
# # print(config.__dict__)
# obj = DataIngestion(data_ingestion_config=config)
# obj.initiate_data_ingestion()