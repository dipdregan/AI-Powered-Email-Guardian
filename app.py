from flask import Flask, render_template, request
import tensorflow as tf
from src.utils import preprocess_data, data_cleaning

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model(r'accepted_models/accepted_model.h5')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form['message']
        # processed_message = data_cleaning(message) 
        prediction = predict_spam_ham(message)
        return render_template('index.html', message=message, prediction=prediction)
    else:
        return render_template('index.html', message='', prediction='')

def predict_spam_ham(message):
    test_padded = preprocess_data([message])  
    prediction_prob = model.predict(test_padded)[0][0]
    threshold = 0.5
    if prediction_prob > threshold:
        return 'Spam'
    else:
        return 'Ham'

if __name__ == '__main__':
    app.run(debug=True)
