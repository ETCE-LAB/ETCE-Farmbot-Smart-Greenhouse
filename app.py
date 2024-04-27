import csv
import time
import ttn
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
csv_file_path = 'ttn_data.csv'

app_id = "eui-70b3d57ed005ea4a"
access_key = "NNSXS.DWWKJ3GCY4SX6SYXOFIHEA2SUMFRC6UQSE7BFFI.YAJWGXZJTYZAXKPE7NJBF6MDPMGH5CNYAZ4XHHBUIETCGFLA4EEA"


def uplink_callback(msg, client):
    print("Received uplink from ", msg.dev_id)
    print(msg)
    # Write to CSV
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([msg.dev_id, msg.payload_raw, msg.metadata.time])


# Setup TTN MQTT Client
handler = ttn.HandlerClient(app_id, access_key)
mqtt_client = handler.data()


def scheduled_task():
    mqtt_client.set_uplink_callback(uplink_callback)
    mqtt_client.connect()
    time.sleep(60)  # Keep the connection open for 60 seconds
    mqtt_client.close()
    print("MQTT client ran for 60 seconds.")


# Initialize CSV file with headers
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Device ID', 'Payload', 'Timestamp'])

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', minutes=15)  # Runs every 15 minutes
scheduler.start()


@app.route('/')
def home():
    return "Scheduler is running and listening to TTN!"


if __name__ == '__main__':
    app.run(debug=True)
