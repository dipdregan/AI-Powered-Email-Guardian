
---

# Ham-Spam Classifier

## Description
The Ham-Spam Classifier is a machine learning project designed to classify SMS messages as either "ham" (legitimate) or "spam" (unsolicited). It utilizes various natural language processing (NLP) techniques and machine learning algorithms to achieve accurate classification.

## Installation
To install the Ham-Spam Classifier, follow these steps:

1. Clone the repository:
   ```
   git clone <repository_url>
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To use the Ham-Spam Classifier, follow these steps:

1. Ensure that you have installed all dependencies as described in the Installation section.
2. Run the main pipeline script:
   ```
   python main_pipeline/main_pipeline.py
   ```
3. Follow the prompts to ingest data, validate, transform, and train the model.
4. Once the pipeline is complete, you can use the trained model for classifying new SMS messages.

## Project Structure
```
config/
│   config.py
│   params.py
│
src/
│
├── components/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── data_validation.py
│   ├── data_transformation.py
│   └── model_trainer.py
│
├── constants/
│   ├── __init__.py
│   ├── constants.py
│   ├── emoji.py
│   └── short_form.py
│
├── entity/
│   ├── __init__.py
│   ├── config_entity.py
│   └── artifact_entity.py
│
├── main_pipeline/
│   ├── main_pipeline.py
│   └── __init__.py
│
├── model_factory/
│   ├── __init__.py
│   └── model_factory.py
│
├── utils/
│   ├── __init__.py
│   └── utils.py
│
├── logger.py
└── exception.py
```

## Components
- **config/**: Contains configuration files.
- **src/components/**: Contains modules for different components of the classifier.
- **src/constants/**: Contains modules for storing constants.
- **src/entity/**: Contains modules defining entities used in the project.
- **src/main_pipeline/**: Contains the main pipeline script.
- **src/model_factory/**: Contains modules related to model creation and management.
- **src/utils/**: Contains utility functions.
- **src/logger.py**: Logger configuration for logging events in the project.
- **src/exception.py**: Custom exception classes for error handling.

## Models
The Ham-Spam Classifier employs the following models:
- Long Short-Term Memory (LSTM)
- Recurrent Neural Network (RNN)
- Combined Model (utilizing both LSTM and RNN)

## Achieved Accuracy
The classifier has achieved an accuracy of 95% on the test dataset.

## Development
Contributions to the Ham-Spam Classifier project are welcome. Here's how you can contribute:
- Fork the repository.
- Create a new branch (`git checkout -b feature`)
- Make your changes and commit them (`git commit -am 'Add new feature'`)
- Push to the branch (`git push origin feature`)
- Create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README file template to better fit your project's specifics and requirements.