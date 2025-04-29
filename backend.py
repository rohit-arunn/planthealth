from flask import Flask, render_template, jsonify
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os
import pickle
app = Flask(__name__)

with open('plant_health_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    try:
        df = pd.read_csv('sensor_data.csv')
        last_data = df.tail(20)  # Last 20 readings
        return jsonify({
            "labels": last_data["timestamp"].tolist(),
            "moisture": last_data["moisture"].tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/confusion-matrix')
def confusion_matrix_route():
    try:
        df = pd.read_csv('sensor_data.csv')
        X_full = df[['temperature', 'humidity', 'moisture']]
        y_true = model.predict(X_full)  # Ideally you need true labels but assuming prediction here

        cm = confusion_matrix(y_true, y_true)  # (This is dummy! You should have real y_true labels.)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot()

        # Save confusion matrix as an image
        if not os.path.exists('static'):
            os.makedirs('static')
        plt.savefig('static/confusion_matrix.png')
        plt.close()
        
        return jsonify({"image_path": "/static/confusion_matrix.png"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
