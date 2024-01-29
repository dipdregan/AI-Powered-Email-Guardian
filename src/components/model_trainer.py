import json
import logging
import pandas as pd
import os,sys
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, SpatialDropout1D
from tensorflow.keras.callbacks import EarlyStopping
from src.constant.constants import *

from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from src.logger import logging
from src.exception import ham_spam
from src.utils import write_json  # Import your utility function

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        self.train_data_path = data_transformation_artifact.train_file_path
        self.test_data_path = data_transformation_artifact.test_file_path

        self.__params = self.model_trainer_config.params['model_params']
        self.__data_processing_params = self.__params['data_processing']
        self.__model_training_params = self.__params['model_training']

        self.__max_words = self.__data_processing_params['max_words']
        self.__max_sequence_length = self.__data_processing_params['max_sequence_length']
        self.__batch_size = self.__model_training_params['batch_size']
        self.__epochs = self.__model_training_params['epochs']
        self.__activation = self.__model_training_params['activation']
        self.__optimizer = self.__model_training_params['optimizer']
        self.__loss = self.__model_training_params['loss']
        self.__validation_split = self.__model_training_params['validation_split']
        self.__patience = self.__model_training_params['patience']
        self.model = None

    def _load_data(self):
        train_data = pd.read_csv(self.train_data_path)
        test_data = pd.read_csv(self.test_data_path)

        train_texts, train_labels = train_data[FEATURES_NAME], train_data[TARGET_NAME]
        test_texts, test_labels = test_data[FEATURES_NAME], test_data[TARGET_NAME]

        return train_texts, train_labels, test_texts, test_labels

    def _preprocess_text(self):
        self.tokenizer = Tokenizer(num_words=self.__max_words, oov_token="null")
        logging.info("loading the data from....>>>")
        logging.info(self.train_data_path)
        logging.info(self.test_data_path)

        train_texts, train_labels, test_texts, test_labels = self._load_data()

        logging.info("tokening the data set...")
        self.tokenizer.fit_on_texts(train_texts)

        train_sequences = self.tokenizer.texts_to_sequences(train_texts)
        test_sequences = self.tokenizer.texts_to_sequences(test_texts)

        logging.info("Padding to make sure all sequences have equal length. Needed for proper model input.")
        train_padded = pad_sequences(train_sequences, maxlen=self.__max_sequence_length, padding='post', truncating='post')
        test_padded = pad_sequences(test_sequences, maxlen=self.__max_sequence_length, padding='post', truncating='post')

        return train_padded, train_labels, test_padded, test_labels

    def _build_model(self):
        logging.info('Building the LSTM model======>>>>>>>')
        self.model = Sequential()
        self.model.add(Embedding(input_dim=self.__max_words, output_dim=32, input_length=self.__max_sequence_length))
        self.model.add(SpatialDropout1D(0.2))
        self.model.add(LSTM(64))
        self.model.add(Dense(1, activation=self.__activation))

        logging.info("Model compile started...........")
        self.model.compile(optimizer=self.__optimizer, loss=self.__loss, metrics=['accuracy'])


    def train_model(self):
        train_padded, train_labels, _, _ = self._preprocess_text()
        logging.info("Creating Early stpoing...........>")
        early_stopping = EarlyStopping(monitor='val_loss', patience=self.__patience, restore_best_weights=True)

        logging.info(f"Training the LSTM model for {self.__epochs} epochs...")

        history = self.model.fit(train_padded, train_labels, epochs=self.__epochs, batch_size=self.__batch_size,
                                 validation_split=self.__validation_split, callbacks=[early_stopping])

        logging.info("Training completed.")

        # Log the training history for each epoch
        for epoch, metrics in enumerate(history.history['loss'], start=1):
            log_message = f"Epoch {epoch}/{self.__epochs} - Loss: {history.history['loss'][epoch-1]} - Accuracy: {history.history['accuracy'][epoch-1]} - Val_loss: {history.history['val_loss'][epoch-1]} - Val_accuracy: {history.history['val_accuracy'][epoch-1]}"
            logging.info(log_message)

        # Save the training history to a JSON file
        history_log_dir = self.model_trainer_config.training_history_dir
        os.makedirs(self.model_trainer_config.training_history_dir, exist_ok=True)
        history_log_path = os.path.join(history_log_dir,
                                        TRAINING_HISTORY_FILE_NAME)
        
        training_metrics = {
            'epochs': list(range(1, self.__epochs + 1)),
            'loss': history.history['loss'],
            'accuracy': history.history['accuracy'],
            'val_loss': history.history['val_loss'],
            'val_accuracy': history.history['val_accuracy']
        }
        
        write_json(training_metrics, history_log_path)  

        logging.info(f"Training history saved to {history_log_path}.")

        return history,history_log_path
    
    def _save_model(self):
        try:
            model_save_dir = self.model_trainer_config.model_dir
            os.makedirs(model_save_dir)
            model_save_path =  os.path.join(model_save_dir,MODEL_NAME)
            self.model.save(model_save_path)
            logging.info(f"Model saved to {model_save_path}.")

            return model_save_path
        except Exception as e:
            logging.error(f"Error saving the model: {str(e)}")

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            self._build_model()
            history,history_log_path = self.train_model()
            model_file_path = self._save_model()
            
            logging.info(history.history)
            model_trainer_artifact = ModelTrainerArtifact(
                model_file_path=model_file_path,
                training_report_file_path = history_log_path
                )
        except Exception as e:
            raise ham_spam(sys,e) from e
            
















# import numpy as np

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Embedding, LSTM, Dense, SpatialDropout1D
# from tensorflow.keras.callbacks import EarlyStopping
# from src.entity.config_entity import *
# from src.entity.artifact_entity import DataTransformationArtifact

# # Load your preprocessed train_data and test_data
# train_data = pd.read_csv(r'artifact\01_29_2024_19_16_48\data_transformation\train_test_data\train.csv')  # Adjust the path
# test_data = pd.read_csv(r'artifact\01_29_2024_19_16_48\data_transformation\train_test_data\test.csv')  # Adjust the path

# # Assuming 'Text_Message' contains the preprocessed text and 'Target' is the label
# train_texts = train_data['Text_Message']
# train_labels = train_data['Target']
# test_texts = test_data['Text_Message']
# test_labels = test_data['Target']

# print(train_texts.shape)
# print(train_labels.shape)
# print(test_texts.shape)
# print(test_labels.shape)

# max_words = 1000  
# tokenizer = Tokenizer(num_words=max_words, oov_token="null")
# tokenizer.fit_on_texts(train_texts)

# train_sequences = tokenizer.texts_to_sequences(train_texts)
# test_sequences = tokenizer.texts_to_sequences(test_texts)

# max_sequence_length = 30
# train_padded = pad_sequences(train_sequences, maxlen=max_sequence_length, padding='post', truncating='post')
# test_padded = pad_sequences(test_sequences, maxlen=max_sequence_length, padding='post', truncating='post')

# model = Sequential()
# model.add(Embedding(input_dim=max_words, output_dim=32, input_length=max_sequence_length))
# model.add(SpatialDropout1D(0.2))
# model.add(LSTM(64))
# model.add(Dense(1, activation='sigmoid'))

# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
# history = model.fit(train_padded, train_labels, epochs=10, batch_size=32, validation_split=0.1, callbacks=[early_stopping])