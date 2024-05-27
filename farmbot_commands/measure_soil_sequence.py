from datetime import datetime
from farmbot import Farmbot, FarmbotToken
import config
from urllib.error import HTTPError
from DataLayer.Models.models import SensorData
from app import app, db


def get_farmbot_token(email, password, url):
    try:
        raw_token = FarmbotToken.download_token(email, password, url)
        return raw_token
    except HTTPError as e:
        error_message = e.read().decode()
        print(f"HTTP Error {e.code}: {error_message}")
        exit(1)


class SensorOperationsHandler:
    def __init__(self, sensor_pickup, pre_pickup, post_pickup, measurement_points, pre_store, sensor_store):
        self.sensor_pickup = sensor_pickup
        self.pre_pickup = pre_pickup
        self.post_pickup = post_pickup
        self.measurement_points = measurement_points
        self.pre_store = pre_store
        self.sensor_store = sensor_store
        self.current_point = 0

    def on_connect(self, bot, mqtt_client):
        bot.move_absolute(*self.pre_pickup)  # Move to safe Z position before picking up the sensor
        print("Connected to FarmBot. Approaching sensor pickup position safely...")

    def on_change(self, bot, state):
        pos = state["location_data"]["position"]
        xyz = (pos["x"], pos["y"], pos["z"])

        if xyz == self.pre_pickup:
            bot.move_absolute(*self.sensor_pickup)
        elif not self.current_point and xyz == self.sensor_pickup:
            bot.move_absolute(*self.post_pickup)  # Move slightly on X-axis to pull out the sensor
            print("Sensor picked up. Adjusting position...")
        elif xyz == self.post_pickup:
            print("Proceeding to measurement points...")
            self.move_to_next_point(bot)
        elif self.current_point < len(self.measurement_points) and xyz == self.measurement_points[self.current_point]:
            self.perform_measurement(bot, xyz)
            self.current_point += 1
            if self.current_point < len(self.measurement_points):
                self.move_to_next_point(bot)
            else:
                bot.move_absolute(*self.pre_store)  # Move slightly before storing the sensor
                print("Measurements complete. Preparing to return sensor.")
        elif xyz == self.pre_store:
            bot.move_absolute(*self.sensor_store)
        elif self.current_point == len(self.measurement_points) and xyz == self.sensor_store:
            print("Sensor returned to storage. Operations completed.")
            bot.disconnect()

    def perform_measurement(self, bot, xyz):  # TODO: Add sensor reading logic
        with app.app_context():
            measurement = SensorData(
                measurement_value=42,  # Simulated sensor value for testing db storage
                measurement_type="Soil Moisture",
                received_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            db.session.add(measurement)
            db.session.commit()
            print(f"Measurement at {xyz} stored in database: {measurement}")

    def move_to_next_point(self, bot):
        bot.move_absolute(*self.measurement_points[self.current_point])
        print(f"Moving to measurement point {self.current_point + 1}...")

    def on_log(self, bot, log):
        print("FarmBot: " + log['message'])

    def on_response(self, bot, response):
        print("Successful request ID: " + response.id)

    def on_error(self, bot, response):
        print("Failed request ID: " + response.id + ", Reason: " + str(response.errors))


# Define sensor pickup adjustments and measurement points
pre_pickup_position = (100, 100, 10)  # Safe Z position before picking up the sensor
sensor_pickup_position = (100, 100, 0)  # Sensor pickup position
post_pickup_position = (110, 100, 0)  # Slight X adjustment after pickup
pre_store_position = (90, 100, 0)  # Slight X adjustment before storing
sensor_store_position = (100, 100, 0)  # Sensor storage position
measurement_points = [(200, 200, -10), (300, 300, -10), (400, 400, -10), (500, 500, -10)]


def execute_measurement_sequence():
    token = get_farmbot_token(config.farmbot_email, config.farmbot_password, config.farmbot_url)
    fb = Farmbot(token)
    handler = SensorOperationsHandler(sensor_pickup_position, pre_pickup_position, post_pickup_position,
                                      measurement_points, pre_store_position, sensor_store_position)
    fb.connect(handler)
