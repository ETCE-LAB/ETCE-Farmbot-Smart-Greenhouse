from flask import Flask, jsonify
from flask_restx import Api, Resource, fields
import json
import requests
import csv
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import config

app = Flask(__name__)
api = Api(app, version='1.0', title='FarmBot Weather API',
          description='Data Endpoint for FarmBot')

# Swagger data model definition for API documentation
message_model = api.model('Message', {
    'Measurement Value': fields.String(required=True, description='The measurement value'),
    'Type': fields.String(required=True, description='Type of measurement'),
    'Received At': fields.String(required=True, description='Date and time of measurement reception')
})

ns = api.namespace('weather', description='Weather operations')


@ns.route('/')
class Home(Resource):
    def get(self):
        return "Weather Station Endpoint for FarmBot. Try /fetch or /data."


@ns.route('/data')
class Data(Resource):
    @api.doc(responses={200: 'Success', 404: 'File Not Found', 500: 'Internal Server Error'})
    @api.marshal_with(message_model, envelope='data', as_list=True)  # Use marshal_with for automatic serialization
    def get(self):
        try:
            data = csv_to_json('weather_data.csv')
            return data, 200
        except FileNotFoundError:
            api.abort(404, 'File not found')
        except Exception as e:
            api.abort(500, str(e))


@ns.route('/fetch')
class Fetch(Resource):
    @api.doc(responses={200: 'Data Fetched Successfully'})
    def get(self):
        fetch_and_process_data()
        return {'status': 'fetched data successfully'}, 200


def fetch_and_process_data():
    print(f"Fetching data at {datetime.datetime.now().strftime('%m-%d %H:%M')}")
    headers = {
        'Authorization': f'Bearer {config.access_key}',
        'Accept': 'application/json'
    }
    response = requests.get(config.device_url, headers=headers)
    if response.status_code == 200:
        print("Data retrieval successful, processing data...")
        handle_partial_json(response.text)
    else:
        print("Failed to retrieve data:", response.status_code, response.text)


def handle_partial_json(text):
    try:
        index = text.rfind('{"result"')
        data = json.loads(text[index:])
        messages = data['result']['uplink_message']['decoded_payload']['messages']
        received_at = data['result']['received_at']
        with open('weather_data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for message in messages:
                writer.writerow([message['measurementValue'], message['type'], received_at])
        print("Weather data written to CSV successfully.")
        print("Awaiting next data fetch...")
    except Exception as e:
        print("Failed to parse truncated JSON:", str(e))


def csv_to_json(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)  # Fetch data every 15 minutes
scheduler.start()

# Initialize CSV file on application startup
with open('weather_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Measurement Value', 'Type', 'Received At'])

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler shut down successfully!")
