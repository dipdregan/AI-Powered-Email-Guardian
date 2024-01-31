from src.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.exception import ham_spam
from src.logger import logging
from src.constant.constants import *
import os
import sys
import pandas as pd
from src.models.label_encoding import LabelConverter
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from src.utils import *
import numpy as np


# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        self.config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact

        self.params = PARAMS_FILE['model_params']['data_processing']
        self.__max_words = self.params['max_words']
        self.__max_sequence_length = self.params['max_sequence_length']

        self.__clean_data_col_name = CONFIG_FILE['clean_data_col_name']



    def _read_data(self, file_path: str) -> pd.DataFrame:
        logging.info(f"Reading data from: {file_path}")
        return pd.read_csv(file_path)

    def _label_encode_target(self, df: pd.DataFrame) -> pd.DataFrame:
        label_converter = LabelConverter()
        df[TARGET_NAME] = df[TARGET_NAME].apply(lambda x: label_converter.ham if x == 'ham' else label_converter.spam)
        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        total_number_of_duplicates = df.duplicated().sum()
        logging.info(f"Number of duplicateds inside the dataset :{total_number_of_duplicates}")
        df = df.drop_duplicates(keep='first')
        return df


    def __data_cleaning(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        logging.info(f"Converting the text in to lower for........................>>>>>")
        logging.info("full filling the Sort form into full form....................>>>>>>>>>>")
        logging.info(f"Removing the EMOJIS from the data set...................>>>>>>>>>>>")
        logging.info("Removing the Stop words................>>>>>>>>>>>>>>")
        logging.info("Converting the text into Root words using Lemmatizer............>>>>")
        logging.info("Data Transformation Completed.....................>>>>>>>>>")
        df[self.__clean_data_col_name] = df[column].apply(data_cleaning)

        return df

    def _preprocess_data(self, df, max_words=6000, max_len=70, column_name:str=None):
        # Tokenization
        tokenizer = Tokenizer(num_words=max_words)
        tokenizer.fit_on_texts(df[column_name])
        sequences = tokenizer.texts_to_sequences(df[column_name])
        padded_sequences = pad_sequences(sequences, maxlen=max_len)
        return tokenizer, padded_sequences


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info(f"{30*'===='}")
            logging.info(f"{10*'=='}Data Transformation Started...{10*'=='}")
            logging.info(f"{30*'===='}")

            df = self._read_data(self.data_validation_artifact.validated_data_path)
            # df = self._read_data(self.data_validation_artifact)
            df = self._label_encode_target(df)
            # logging.info(f"Data :\n {df.head()}")
            df = self._remove_duplicates(df)

            clean_df = self.__data_cleaning(df,FEATURES_NAME)
            # data = df.dropna(subset=[FEATURES_NAME])
            # logging.info(f"\n{clean_df}")

            os.makedirs(self.config.transform_dir_path, exist_ok=True)
            transformed_data_path = os.path.join(self.config.transform_dir_path,
                                                TRANSFORM_DATA_FILE_NAME)
            
            save_data(clean_df, transformed_data_path)

            tokenizer, padded_sequences = self._preprocess_data(clean_df,
                                                                self.__max_words,
                                                                self.__max_sequence_length,
                                                                self.__clean_data_col_name
                                                            )
            logging.info(len(padded_sequences))
            logging.info(padded_sequences[0])


            feature_label_data_dir = self.config.feature_data_file_path
            os.makedirs(feature_label_data_dir, exist_ok= True)

            feature_data_file_path = os.path.join(feature_label_data_dir,
                                                FEATURES_DATA_FILE_NAME)
            label_data_file_path = os.path.join(feature_label_data_dir,
                                                LABEL_DATA_FIEL_NAME)

            np.save(feature_data_file_path, padded_sequences)

            np.save(label_data_file_path, clean_df[TARGET_NAME].to_numpy())

            preprocess_model_file_path = self.config.preprocess_model_file_path
            os.makedirs(preprocess_model_file_path,exist_ok=True)
            preprocess_model_file_dir = os.path.join(preprocess_model_file_path,
                                                    PREPROCESS_DATA_FILE_NAME)
            save_tokenizer(tokenizer=tokenizer,
                        filename=preprocess_model_file_dir)

            logging.info(f"{30*'===='}")
            logging.info(f"{10*'=='}Data Transformation Completed...{10*'=='}")
            logging.info(f"{30*'===='}")

            data_transformation_artifact = DataTransformationArtifact(
                data_transformation_path=transformed_data_path,
                feature_data_file_path=feature_data_file_path,
                label_data_file_path=label_data_file_path,
                preprocess_file_path=preprocess_model_file_path
            )
            logging.info(data_transformation_artifact)
            return data_transformation_artifact
        except Exception as e:
            raise ham_spam(e, sys) from e

