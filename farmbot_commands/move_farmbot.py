# move_farmbot.py
import json
from urllib.error import HTTPError
from farmbot import Farmbot, FarmbotToken


def get_farmbot_token(email, password, url):
    try:
        raw_token = FarmbotToken.download_token(email, password, url)
        return raw_token
    except HTTPError as e:
        error_message = e.read().decode()
        print(f"HTTP Error {e.code}: {error_message}")
        exit(1)


class MyHandler:
    def __init__(self, target_x, target_y, target_z):
        self.target_x = target_x
        self.target_y = target_y
        self.target_z = target_z

    def on_connect(self, bot, mqtt_client):
        request_id1 = bot.move_absolute(x=self.target_x, y=self.target_y, z=self.target_z)
        print("MOVE_ABS REQUEST ID: " + request_id1)

    def on_change(self, bot, state):
        print("Current position: (%.2f, %.2f, %.2f)" % bot.position())
        pos = state["location_data"]["position"]
        xyz = (pos["x"], pos["y"], pos["z"])

        if xyz == (self.target_x, self.target_y, self.target_z):
            print(
                f"FarmBot has reached the coordinates ({self.target_x}, {self.target_y}, {self.target_z}). Stopping the script.")
            raise KeyboardInterrupt

    def on_log(self, bot, log):
        print("New message from FarmBot: " + log['message'])

    def on_response(self, bot, response):
        print("ID of successful request: " + response.id)

    def on_error(self, bot, response):
        print("ID of failed request: " + response.id)
        print("Reason(s) for failure: " + str(response.errors))


def move_to(x, y, z):
    email = "a.kannenberg@ostfalia.de"
    password = "DigitFarmBot2024!"
    url = "https://my.farm.bot"

    token = get_farmbot_token(email, password, url)
    fb = Farmbot(token)

    handler = MyHandler(x, y, z)
    try:
        fb.connect(handler)
    except KeyboardInterrupt:
        # Clean up and exit
        return {
            'status': 'FarmBot has reached the target coordinates',
            'x': x,
            'y': y,
            'z': z
        }
