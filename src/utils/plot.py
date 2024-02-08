import os
import itertools
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
from src.logger import logging

def plot_confusion_matrix(cm, classes, title='Confusion matrix',
                           cmap=plt.cm.Blues, label_converter=None,save_path=None):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = range(len(classes))
    plt.xticks(tick_marks, [label_converter.decode(label) for label in classes], rotation=45)
    plt.yticks(tick_marks, [label_converter.decode(label) for label in classes])

    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, 'confusion_matrix.png'))
    plt.close()

def plot_training_history(history, save_path,model_type):
    # Plot training & validation accuracy values
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.savefig(os.path.join(save_path, f'{model_type}_training_history_accuracy.png'))
    plt.close()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.savefig(os.path.join(save_path, f'{model_type}_training_history_loss.png'))
    plt.close()

def compute_classification_report(y_true, y_pred, label_converter, save_path):
    classification_rep = classification_report(y_true, y_pred, target_names=[label_converter.decode(0), label_converter.decode(1)])
    with open(os.path.join(save_path, 'classification_report.txt'), 'w') as report_file:
        report_file.write(classification_rep)
