import json
from datetime import datetime
import requests
import config
from DataLayer.Models.WeatherStationModel import WeatherStationData
from DataLayer.WeatherStationRepository import add_weather_data
from app import app


def fetch_weather_station_data():
    with app.app_context():
        headers = {
            'Authorization': f'Bearer {config.weatherstation_access_key}'
        }
        response = requests.get(config.weatherstation_device_url, headers=headers)
        if response.status_code == 200:
            print(datetime.now().strftime('%d-%m %H:%M') + " Station fetch successful, saving...")
            handle_partial_json(response.text)
            return {'message': "Data fetched and saved successfully", 'code': 200}
        else:
            error_message = f"Failed to retrieve data with status code {response.status_code}"
            print(error_message)
            print(response.text)
            return {'message': error_message, 'code': response.status_code}


def handle_partial_json(text):
    with app.app_context():
        index = text.rfind('{"result"')
        data = json.loads(text[index:])
        messages = data['result']['uplink_message']['decoded_payload']['messages']
        received_at = data['result']['received_at']
        fetched_at = datetime.now()

        for message in messages:
            weather_data = WeatherStationData(
                measurement_value=message['measurementValue'],
                measurement_type=message['type'],
                received_at=received_at,
                fetched_at=fetched_at
            )
            add_weather_data(weather_data)
        #commit_changes()
