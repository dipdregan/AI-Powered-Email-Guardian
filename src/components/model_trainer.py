import json
import logging
import pandas as pd
import os, sys
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint
from src.utils.plot import plot_training_history
from src.constant.constants import *
import pandas as pd
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from src.model_factory.model_factory import ModelFactory
from src.logger import logging
from src.exception import ham_spam
from src.utils.utils import *
import numpy as np

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

        self._X = data_transformation_artifact.feature_data_file_path
        self._y = data_transformation_artifact.label_data_file_path

        self._model_training_params = PARAMS_FILE['model_params']['model_training']
        self._batch_size = self._model_training_params['batch_size']
        self._epochs = self._model_training_params['epochs']
        self._validation_split = self._model_training_params['validation_split']
        self._patience = self._model_training_params['patience']
        self.model = None
        self.model_factory = ModelFactory()

    def train_model(self, X_train, y_train, model_type):
        logging.info(f"Creating Early stopping for {model_type} model...")
        early_stopping = EarlyStopping(monitor='val_loss', 
                                       patience=self._patience, 
                                       restore_best_weights=True
                                       )

        # Build the model using ModelFactory
        self.model = self.model_factory.build_model_type(model_type)

        logging.info(f"Training the {model_type} model for {self._epochs} epochs...")
        history = self.model.fit(X_train, y_train,
                                epochs=self._epochs, batch_size=self._batch_size,
                                validation_split=self._validation_split,
                                callbacks=[early_stopping])

        # Log training history and save to file
        for epoch, metrics in enumerate(history.history['loss'], start=1):
            log_message = f"Epoch {epoch}/{self._epochs} - Loss: {history.history['loss'][epoch-1]} - Accuracy: {history.history['accuracy'][epoch-1]} - Val_loss: {history.history['val_loss'][epoch-1]} - Val_accuracy: {history.history['val_accuracy'][epoch-1]}"

            logging.info(log_message)

        history_log_dir = self.model_trainer_config.training_history_dir
        os.makedirs(self.model_trainer_config.training_history_dir, exist_ok=True)
        history_log_path = os.path.join(history_log_dir, 
                                        f"{model_type}_{TRAINING_HISTORY_FILE_NAME}")

        training_metrics = {
            'epochs': list(range(1, self._epochs + 1)),
            'loss': history.history['loss'],
            'accuracy': history.history['accuracy'],
            'val_loss': history.history['val_loss'],
            'val_accuracy': history.history['val_accuracy']
        }

        write_json(training_metrics, history_log_path)
        logging.info(f"Training history saved to {history_log_path}.")

        training_report_graph = self.model_trainer_config.training_report
        os.makedirs(self.model_trainer_config.training_report,exist_ok=True)
        plot_training_history(history,training_report_graph,model_type)

        return  history_log_path,training_report_graph

    def _save_model(self,model_type):
        try:
            model_save_dir = self.model_trainer_config.model_dir
            os.makedirs(model_save_dir, exist_ok=True)
            model_save_path = os.path.join(model_save_dir, f"{model_type}.h5")
            self.model.save(model_save_path)
            logging.info(f"{model_type} Model saved to {model_save_path}.")
            return model_save_path
        except Exception as e:
            logging.error(f"Error saving the model: {str(e)}")

    def initiate_model_trainer(self, model_types=['lstm', 'rnn', 'combined']):
        artifacts = []
        X_train,y_train, X_test, y_test = load_and_split_data(self._X,self._y)
        
        for model_type in model_types:
            try:
                history_log_path,training_report_graph =self.train_model(
                    X_train, y_train, model_type=model_type
                    )

                model_file_path = self._save_model(model_type=model_type)
                history_log_path = os.path.join(self.model_trainer_config.training_history_dir,
                                                f"{model_type}_{TRAINING_HISTORY_FILE_NAME}")
                
                
            except Exception as e:
                logging.error(f"Error during training {model_type} model: {str(e)}")

        model_trainer_artifact = ModelTrainerArtifact(
                    model_file_path=self.model_trainer_config.model_dir,
                    training_report_file_path=history_log_path,
                    training_report_graph = training_report_graph
                )
        logging.info(model_trainer_artifact)
        artifacts.append(model_trainer_artifact)
        return model_trainer_artifact
    

    