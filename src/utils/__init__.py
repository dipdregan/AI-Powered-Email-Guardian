import yaml
import pandas as pd
from src.exception import ham_spam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.stem import SnowballStemmer
from src.constant.emoji import emoji_pattern
from src.constant.short_form import short_forms
import re
from nltk.tokenize import word_tokenize
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def read_yaml_file(file_path):
    """
    Read and parse content from a YAML file.
    """
    with open(file_path, 'r') as yaml_file:
        try:
            data = yaml.safe_load(yaml_file)
            return data
        except yaml.YAMLError as e:
            print(f"Error reading YAML file {file_path}: {e}")
            return None

import json

def read_json(file_path):
    """
    Read data from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - data (dict): The data read from the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from file: {file_path}")

def write_json(data, file_path):
    """
    Write data to a JSON file.

    Parameters:
    - data (dict): The data to be written to the JSON file.
    - file_path (str): The path to the JSON file.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        raise ValueError(f"Error writing JSON to file: {file_path}. {str(e)}")


import pickle

def read_pickle(file_path):
    """Read a pickle file."""
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
        return data
    except Exception as e:
        raise ValueError(f"Error reading pickle file: {e}")

def write_pickle(data, file_path):
    """Write data to a pickle file."""
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
    except Exception as e:
        raise ValueError(f"Error writing to pickle file: {e}")


def write_pickle(data, file_path):
    """Write data to a pickle file."""
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
    except Exception as e:
        raise ValueError(f"Error writing to pickle file: {e}")


def load_data(test_data_path,feature_name,target):
    try:
        test_data = pd.read_csv(test_data_path)
        feature, labels = test_data[feature_name], test_data[target]
        return feature, labels
    except Exception as e:
        raise ham_spam(e) from e

def preprocess_data(feature,max_words=100,max_sequence_length=30):
    try:
        tokenizer = Tokenizer(num_words=max_words, oov_token="null")
        tokenizer.fit_on_texts(feature)
        test_sequences = tokenizer.texts_to_sequences(feature)
        feature_padded = pad_sequences(test_sequences, maxlen=max_sequence_length,
                                    padding='post', truncating='post')
        return feature_padded
    except Exception as e:
        raise ham_spam(e) from e
    
def data_cleaning(text: str) -> str:
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
    
    stemmer = SnowballStemmer("english")
    
    words = [stemmer.stem(word) for word in word_tokenize(text) if word.lower() not in stop_words]
    
    return ' '.join(words)

