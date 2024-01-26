from src.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.exception import ham_spam
from src.logger import logging
from src.constant.constants import TARGET_NAME,FEATURES_NAME
import os
import sys
import pandas as pd
from src.models.label_encoding import LabelConverter
from src.constant.emoji import emoji_pattern
from src.constant.short_form import short_forms
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# nltk.download('punkt')


class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        self.data_transformation_config = data_transformation_config
        self.data_validation_artifact = data_validation_artifact

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

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess the input text:
        1. Convert text to lowercase
        2. Replace short forms with their full forms
        3. Removing emojis
        4. Removing non-alphanumeric characters (commented out)
        5. Removing stop words
        6. Lemmatizing the words in to root word

        """
        text = text.lower()
        for short_form, full_form in short_forms.items():
            text = re.sub(r'\b{}\b'.format(re.escape(short_form)), full_form, text)

        text = emoji_pattern.sub(r'', text)
        # text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        stop_words = set(stopwords.words('english'))
        
        lemmatizer = WordNetLemmatizer()
        
        words = [lemmatizer.lemmatize(word) for word in word_tokenize(text) if word.lower() not in stop_words]
        
        return ' '.join(words)

    def _preprocess_text_column(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        logging.info(f"Converting the text in to lower for........................>>>>>")
        logging.info("full filling the Sort form into full form....................>>>>>>>>>>")
        logging.info(f"Removing the EMOJIS from the data set...................>>>>>>>>>>>")
        logging.info("Removing the Stop words................>>>>>>>>>>>>>>")
        logging.info("Converting the text into Root words using Lemmatizer............>>>>")
        logging.info("Data Transformation Completed.....................>>>>>>>>>")
        df[column] = df[column].apply(self._preprocess_text)

        return df

    def _save_transformed_data(self, df: pd.DataFrame, save_path: str) -> None:
        df.to_csv(save_path, index=False)
        logging.info(f"Saving the Transformed data to: {save_path}")

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        # try:
        logging.info(f"{30*'===='}")
        logging.info(f"{10*'=='}Data Transformation Started...{10*'=='}")
        logging.info(f"{30*'===='}")

        # df = self._read_data(self.data_validation_artifact.validated_data_path)
        df = self._read_data(self.data_validation_artifact)
        df = self._label_encode_target(df)
        logging.info(f"Data :\n {df.head()}")
        df = self._remove_duplicates(df)

        df = self._preprocess_text_column(df, 'Text_Message')

        os.makedirs(self.data_transformation_config.data_transformation_dir, exist_ok=True)
        transformed_data_path = os.path.join(self.data_transformation_config.data_transformation_dir,
                                            self.data_transformation_config.data_transformation_file_name)
        self._save_transformed_data(df, transformed_data_path)


        logging.info(f"{30*'===='}")
        logging.info(f"{10*'=='}Data Transformation Completed...{10*'=='}")
        logging.info(f"{30*'===='}")

        data_transformation_artifact = DataTransformationArtifact(
            data_transformation_path=transformed_data_path
        )

        return data_transformation_artifact
    

        # except Exception as e:
        #     raise ham_spam(e, sys) from e

