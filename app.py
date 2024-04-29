from flask import Flask, jsonify
import json
import requests
import csv
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import config

app = Flask(__name__)


def fetch_and_process_data():
    print(f"Fetching data at {datetime.datetime.now().strftime('%m-%d %H:%M')}")
    response = requests.get(config.device_url, headers=headers)
    if response.status_code == 200:
        print("Data retrieval successful, processing data...")
        handle_partial_json(response.text)
    else:
        print("Failed to retrieve data:", response.status_code, response.text)


def handle_partial_json(text):
    try:
        index = text.rfind('{"result"')
        #  print(text[index:])
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


# Function to convert CSV to JSON
def csv_to_json(filename):
    data = []
    with open(filename, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


# Endpoint to for getting data
@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = csv_to_json('weather_data.csv')
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)  # Set interval here
scheduler.start()


#  Endpoint to fetch data immediately
@app.route('/fetch', methods=['GET'])
def start_fetching():
    fetch_and_process_data()
    return jsonify({'status': 'fetched data successfully'})


# Headers for API request
headers = {
    'Authorization': f'Bearer {config.access_key}',
    'Accept': 'application/json'
}

# Initialize CSV
with open('weather_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Measurement Value', 'Type', 'Received At'])

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler shut down successfully!")
