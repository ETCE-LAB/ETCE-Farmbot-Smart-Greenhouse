from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import csv
import time
import ttn

app = Flask(__name__)

# Initialize CSV file
csv_file_path = 'ttn_data.csv'
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Device ID', 'Payload', 'Timestamp'])  # Adjust headers based on actual data structure


def scheduled_task():
    app_id = "tuc-isse-sensorik"
    access_key = "NNSXS.BGN4W6LCYDLSGVATWTPPMU7URARU6NO3HCCA4BI.KBHIS4VN65K32UK57QLHP2NA6PXULQ4Y2IWXGHUAN5VIBOZUPQUQ"  # TODO: Hide API key!

    def uplink_callback(msg, client):
        print("Received uplink from ", msg.dev_id)
        print(msg)
        # Write to CSV
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([msg.dev_id, msg.payload_raw, msg.metadata.time])

    handler = ttn.HandlerClient(app_id, access_key)

    mqtt_client = handler.data()
    mqtt_client.set_uplink_callback(uplink_callback)
    mqtt_client.connect()
    time.sleep(60)
    mqtt_client.close()

    print("Executing every 15 minutes.")


scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', minutes=15)
scheduler.start()


@app.route('/')
def home():
    return "Scheduler is running!"


if __name__ == '__main__':
    app.run(debug=True)
