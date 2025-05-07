from flask import Flask, jsonify,render_template, send_from_directory
from flask_cors import CORS
import time
import board
import adafruit_dht
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler


loaded_model = load_model('temperature_lstm_model.h5')

input_sequence = [23, 45, 25, 26, 23, 32, 34]

def predict_temperature(input_sequence, model, look_back=7):
    if len(input_sequence) != look_back:
        raise ValueError(f"Input sequence must be of length {look_back}.")
    
    input_sequence = np.array(input_sequence).reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    input_sequence_scaled = scaler.fit_transform(input_sequence)
    input_sequence_scaled = input_sequence_scaled.reshape(1, look_back, 1)

    predicted_scaled = model.predict(input_sequence_scaled)
    predicted_temp = scaler.inverse_transform(predicted_scaled)
    
    return float(predicted_temp[0][0])


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the DHT device
dht_device = adafruit_dht.DHT11(board.D4)
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/sensor-data')
def get_sensor_data():
    tries = 0
    max_tries = 2
    
    while tries < max_tries:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            predicted_temperature = predict_temperature([temperature+1,temperature,temperature-1,temperature+1,temperature+2,temperature+8,temperature+1], loaded_model)
            if temperature is not None and humidity is not None:
                return jsonify({
                    'temperature': temperature,
                    'humidity': humidity,
                    'predicted': round(predicted_temperature,1)
                })
            
        except RuntimeError as error:
            # Errors happen fairly often with DHT sensors
            print(f"Error reading sensor: {error.args[0]}")
            tries += 1
            time.sleep(2)  # Wait 2 seconds before retrying
            
        except Exception as error:
            print(f"Failed to read sensor: {error}")
            return jsonify({
                'error': 'Failed to read sensor'
            }), 500
    
    return jsonify({
        'error': 'Failed to read sensor after multiple attempts'
    }), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        # Clean up the GPIO pins
        dht_device.exit()
