import json
import requests
import csv
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time


def fetch_and_process_data():
    print(f"Fetching data at {datetime.datetime.now().strftime('%m-%d %H:%M')}")
    response = requests.get(device_url, headers=headers)
    if response.status_code == 200:
        print("Data retrieval successful, processing data...")
        parse_and_save_to_csv(response.text)
    else:
        print("Failed to retrieve data:", response.status_code, response.text)


def parse_and_save_to_csv(text):
    try:
        data = json.loads(text)
        messages = data['result']['uplink_message']['decoded_payload']['messages']
        received_at = data['result']['received_at']

        with open('weather_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Measurement Value', 'Type', 'Received At'])

            for message in messages:
                writer.writerow([message['measurementValue'], message['type'], received_at])

        print("Weather data written to CSV successfully.")
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", str(e))
        handle_partial_json(text, e.pos)
    except Exception as e:
        print("Error during processing:", str(e))


def handle_partial_json(text, error_position):
    try:
        data = json.loads(text[:error_position])
        messages = data['result']['uplink_message']['decoded_payload']['messages']
        received_at = data['result']['received_at']

        with open('weather_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Measurement Value', 'Type', 'Received At'])

            for message in messages:
                writer.writerow([message['measurementValue'], message['type'], received_at])

        print("Partial weather data written to CSV successfully.")
    except Exception as e:
        print("Failed to parse truncated JSON:", str(e))


application_id = 'tuc-isse-sensorik'
device_id = 'eui-70b3d57ed005ea4a'
access_key = 'NNSXS.DWWKJ3GCY4SX6SYXOFIHEA2SUMFRC6UQSE7BFFI.YAJWGXZJTYZAXKPE7NJBF6MDPMGH5CNYAZ4XHHBUIETCGFLA4EEA'
# TODO: Hide API Key

data_type = 'uplink_message'
device_url = f"https://eu1.cloud.thethings.network/api/v3/as/applications/{application_id}/devices/{device_id}/packages/storage/{data_type}"

headers = {
    'Authorization': f'Bearer {access_key}',
    'Accept': 'application/json'
}

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)
scheduler.start()

try:
    while True:
        print("Running..." + " Time: " + time.strftime("%H:%M"))
        time.sleep(70)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler shut down successfully!")
