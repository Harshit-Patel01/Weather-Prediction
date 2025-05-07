# Weather Monitoring and Prediction System

This project is a Raspberry Pi-based weather monitoring system that uses a DHT11 temperature and humidity sensor to collect environmental data and predict future temperature values using a machine learning model.

## Features

- Real-time temperature and humidity monitoring using DHT11 sensor
- Temperature prediction using LSTM (Long Short-Term Memory) neural network
- Modern, responsive web interface with analog clock display
- RESTful API for sensor data retrieval

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- DHT11 temperature and humidity sensor
- Connection wires

## Software Requirements

- Python 3.6+
- Flask
- TensorFlow
- NumPy
- Adafruit DHT library
- scikit-learn

## Installation

1. Clone this repository to your Raspberry Pi:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required Python dependencies:
   ```
   pip install flask flask-cors tensorflow numpy scikit-learn adafruit-circuitpython-dht
   ```

3. Connect the DHT11 sensor to your Raspberry Pi:
   - Connect the sensor's VCC pin to 3.3V or 5V on the Raspberry Pi
   - Connect the sensor's GND pin to GND on the Raspberry Pi
   - Connect the sensor's DATA pin to GPIO4 (Pin 7) on the Raspberry Pi

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://<raspberry-pi-ip-address>:5000
   ```

## How it Works

- The system reads temperature and humidity data from the DHT11 sensor
- The collected data is processed and served via a Flask web application
- A pre-trained LSTM model (`temperature_lstm_model.h5`) is used to predict future temperature values
- The web interface displays current readings, predicted temperatures, and includes an analog clock

## API Endpoints

- `GET /sensor-data`: Returns the current temperature, humidity, and predicted temperature in JSON format

## Files Description

- `app.py`: Main Flask application that serves the web interface and API
- `temperature_lstm_model.h5`: Pre-trained TensorFlow model for temperature prediction
- `index.html`: Main web interface
- `style.css`: Styling for the web interface
- `script.js`: JavaScript for the web interface functionality
- Various SVG files: Graphics for the web interface 