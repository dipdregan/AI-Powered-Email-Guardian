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
