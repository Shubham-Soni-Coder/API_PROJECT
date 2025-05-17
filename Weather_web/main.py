import requests
from flask import Flask, request, send_from_directory, jsonify

# Create a Flask web application instance
app = Flask(__name__)

# Your OpenWeatherMap API key and base URL
api_keys = '9bece2c315ccb96103d66c938f2766f2'
base_url = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    """
    Serve the main HTML page for the weather app.
    """
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    """
    Serve the CSS file for styling the weather app.
    """
    return send_from_directory('.', 'style.css')

@app.route('/weather')
def weather():
    """
    API endpoint to get weather data for a given city.
    Expects a 'city' query parameter from the frontend.
    Returns temperature, humidity, pressure, wind speed, description, and icon as JSON.
    """
    # Get the city name from the query parameters
    city = request.args.get('city')
    if not city:
        # If no city is provided, return an error
        return jsonify({'error': 'City is required'}), 400
    # Prepare parameters for the OpenWeatherMap API request
    params = {
        'q': city,
        'appid': api_keys,
        'units': 'metric'
    }
    # Make a GET request to the OpenWeatherMap API
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        # If the request is successful, extract and return relevant weather data
        return jsonify({
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        })
    else:
        # If the request fails, return the error message from the API
        return jsonify({'error': data.get('message', 'Error fetching weather')}), 400

if __name__ == '__main__':
    """
    Run the Flask development server.
    """
    app.run(debug=True)