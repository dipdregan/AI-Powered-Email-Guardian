import os
import shutil
import json
import tensorflow as tf
from src.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact, ModelEvaluatorArtifact
from src.entity.config_entity import ModelEvaluatorConfig
from src.constant.constants import *
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.utils.utils import write_json, load_and_split_data
from src.utils.plot import plot_confusion_matrix
from src.logger import logging
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

class ModelEvaluator:
    def __init__(self, model_trainer_artifacts: ModelTrainerArtifact,
                 data_transformation_artifact: DataTransformationArtifact,
                 model_evaluation_config: ModelEvaluatorConfig):
        
        self.config = model_evaluation_config
        self.X = data_transformation_artifact.feature_data_file_path
        self.y = data_transformation_artifact.label_data_file_path
        self.model_trainer_artifacts = model_trainer_artifacts.model_file_path
        self.accepted_model_path = None
        self.max_accuracy = 0.0
        self.accepted_model = None

    def model_paths(self):
        models_path = []
        for model_file in os.listdir(self.model_trainer_artifacts):
            models_path.append(os.path.join(self.model_trainer_artifacts, model_file))
        return models_path

    def evaluate_models(self, X_test, y_test):
        models_path = self.model_paths()
        for model_path in models_path:
            model = tf.keras.models.load_model(model_path)
            y_pred = model.predict(X_test)
            
            # Apply thresholding if y_pred contains probabilities
            y_pred_binary = (y_pred > 0.5).astype(int)

            accuracy = accuracy_score(y_test, y_pred_binary)
            if accuracy > self.max_accuracy:
                self.max_accuracy = accuracy
                self.accepted_model_path = model_path

        logging.info(f"Accepted model: {self.accepted_model_path}")
        return self.accepted_model_path
    
    def calculate_evaluation_metrics(self, X_test, y_test):
        model = tf.keras.models.load_model(self.accepted_model_path)
        y_pred = model.predict(X_test)
        
        # Apply thresholding if y_pred contains probabilities
        y_pred_binary = (y_pred > 0.5).astype(int)
        precision = precision_score(y_test, y_pred_binary)
        recall = recall_score(y_test, y_pred_binary)
        f1 = f1_score(y_test, y_pred_binary)

        os.makedirs(self.config.evaluation_report, exist_ok=True)
        plot_path = os.path.join(self.config.evaluation_report, CONFUSION_MATRIX)
        plot_confusion_matrix(y_true=y_test, y_pred=y_pred_binary,classes=['ham','spam'], save_path=plot_path)
        return precision, recall, f1
    
    def initiate_model_evaluation(self) -> ModelEvaluatorArtifact:
        logging.info("============================Model Evaluation Started ================")
        _, _, X_test, y_test = load_and_split_data(X=self.X, y=self.y)
        accepted_model_path = self.evaluate_models(X_test, y_test)
        logging.info(accepted_model_path)
        # Save the accepted model to the accepted directory
        accepted_model_name = os.path.basename(accepted_model_path)
        
        logging.info(accepted_model_name)
        os.makedirs(self.config.accepted_model, exist_ok=True)
        print(self.config.accepted_model)
        accepted_model_destination = os.path.join(self.config.accepted_model, accepted_model_name)
        shutil.copy(accepted_model_path, accepted_model_destination)
        self.accepted_model = accepted_model_destination
        
        # Calculate precision, recall, and F1-score
        precision, recall, f1= self.calculate_evaluation_metrics(X_test, y_test)
        
        # Save evaluation report
        evaluation_report = {
            "accepted_model": accepted_model_destination,
            "accuracy": self.max_accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
        path = os.path.join(self.config.evaluation_report, EVALUATION_REPORT_JSON)
        write_json(evaluation_report, path)
        
        model_evaluation_artifact =  ModelEvaluatorArtifact(
            accepted_model_path=self.accepted_model,
            evaluation_report_path=self.config.evaluation_report
        )
        logging.info(model_evaluation_artifact)
        logging.info("============================Model evaluation completed.================================")
        return model_evaluation_artifact
