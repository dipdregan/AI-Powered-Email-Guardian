import yaml
import pandas as pd
from src.exception import ham_spam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


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


def load_test_data(test_data_path,feature_name,target):
    try:
        test_data = pd.read_csv(test_data_path)
        feature, labels = test_data[feature_name], test_data[target]
        return feature, labels
    except Exception as e:
        raise ham_spam(e) from e

def preprocess_test_data(feature,max_words,max_sequence_length):
    try:
        tokenizer = Tokenizer(num_words=max_words, oov_token="null")
        tokenizer.fit_on_texts(feature)
        test_sequences = tokenizer.texts_to_sequences(feature)
        feature_padded = pad_sequences(test_sequences, maxlen=max_sequence_length,
                                    padding='post', truncating='post')
        return feature_padded
    except Exception as e:
        raise ham_spam(e) from e
    
def confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, 
                                  display_labels=['Class 0', 'Class 1'])
    disp.plot(cmap=plt.cm.Blues, values_format='d')
    plt.savefig('confusion_matrix.png')
    plt.show()

def plot_training_history(history):
    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper right')
    plt.show()

    # Plot training & validation accuracy values
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='lower right')
    plt.show()


