from farmbot import Farmbot
from urllib.error import HTTPError
import config


def get_farmbot_token(email, password, url):
    try:
        raw_token = FarmbotToken.download_token(email, password, url)
        return raw_token
    except HTTPError as e:
        error_message = e.read().decode()
        print(f"HTTP Error {e.code}: {error_message}")
        exit(1)


COORDINATES = {
    'home': (0, 0, 0),
    'soil_sensor_safe': (15, 83, 0),  # -380),
    'soil_sensor': (15, 83, 0),  # -414),
    'point3': (115, 83, 0),  # -414),
    'point4': (400, 600, 0),  # -475),
    'point5': (1000, 600, 0),  # -470),
    'point6': (2100, 600, 0)  # -480)
}


class SoilMoistureHandler:
    def __init__(self, bot):
        self.bot = bot

    def measure_soil_moisture(self):
        # Sequence of points to visit, add or remove points as needed
        points_sequence = [
            'home', 'point1', 'point2', 'point3', 'point4', 'home',
            'point4', 'home', 'point5', 'home', 'point6', 'home',
            'point3', 'point2', 'home'
        ]

        for point in points_sequence:
            x, y, z = COORDINATES[point]
            self.bot.move_absolute(x=x, y=y, z=z)
            print(f"Moving to {point} at coordinates ({x}, {y}, {z})")
            time.sleep(0.1)  # Short wait for move completion; adjust as needed

            if z < 0:  # Assuming we only measure moisture when the z-coordinate is below zero
                self.read_soil_moisture_pin()

    def read_soil_moisture_pin(self):
        # TODO: Implement the actual pin reading logic here and save to database
        print("Reading soil moisture level from sensor...")
        time.sleep(0.3)  # Simulate the wait time after reading


def measure_soil_moisture_sequence():
    email = config.farmbot_email
    password = config.farmbot_password
    url = config.farmbot_url

    token = get_farmbot_token(email, password, url)
    fb = Farmbot(token)
    soil_moisture_handler = SoilMoistureHandler(fb)

    try:
        fb.connect()
        soil_moisture_handler.measure_soil_moisture()
    finally:
        fb.disconnect()
        print("Measurement sequence completed.")


if __name__ == "__main__":
    measure_soil_moisture_sequence()
