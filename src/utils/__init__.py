import yaml

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
