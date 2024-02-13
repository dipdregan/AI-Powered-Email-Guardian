from flask import Flask, render_template, request,jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
from src.utils.utils import data_cleaning, read_json
from src.constant.constants import CONFIG_DIR_NAME, MODEL_REPORT_FILE_NAME
from src.utils.s3_operation_utils import S3_operation

app = Flask(__name__)

path = os.path.join(CONFIG_DIR_NAME, MODEL_REPORT_FILE_NAME)
model_path = read_json(path)
process_model_path = model_path['process_path']
model_path = model_path['model_path']

tokenizer = S3_operation().load_process_model(process_model_path)
model = S3_operation().load_model(model_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        messages = request.form.getlist('message')
        predictions = []
        for message in messages:
            y_pred_prob, y_pred, message = prediction(message)
            predictions.append({'message': message, 'prediction': y_pred_prob[0], 'probability': float(y_pred[0][0])})
        return  jsonify(predictions=predictions)
    else:
        return render_template('index.html', predictions=[])

def prediction(message):
    clean = data_cleaning(message)
    seq = tokenizer.texts_to_sequences([clean])
    padded_seq = pad_sequences(seq, maxlen=60)
    y_pred = model.predict(padded_seq)
    y_pred_prob = ['spam' if pred >= 0.5 else 'ham' for pred in y_pred]
    return y_pred_prob, y_pred, message

if __name__ == '__main__':
    app.run(debug=True)
