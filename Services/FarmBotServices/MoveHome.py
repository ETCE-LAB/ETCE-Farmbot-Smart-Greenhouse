from farmbot import Farmbot, FarmbotToken
import config
from urllib.error import HTTPError


def get_farmbot_token(email, password, url):
    try:
        raw_token = FarmbotToken.download_token(email, password, url)
        return raw_token
    except HTTPError as e:
        error_message = e.read().decode()
        print(f"HTTP Error {e.code}: {error_message}")
        exit(1)


class MoveHome:
    def __init__(self, target_x, target_y, target_z):
        self.target_x = 0
        self.target_y = 0
        self.target_z = 0

    def on_connect(self, bot, mqtt_client):
        bot.move_absolute(x=self.target_x, y=self.target_y, z=self.target_z)
        bot.send_message("Moving to target coordinates...")

    def on_change(self, bot, state):
        print("Current position: (%.2f, %.2f, %.2f)" % bot.position())
        pos = state["location_data"]["position"]
        xyz = (pos["x"], pos["y"], pos["z"])

        if xyz == (self.target_x, self.target_y, self.target_z):
            print(
                f"FarmBot has reached the coordinates ({self.target_x}, {self.target_y}, {self.target_z}). Disconnecting from FarmBot.")
            raise KeyboardInterrupt

    def on_log(self, bot, log):
        print("New message from FarmBot: " + log['message'])

    def on_response(self, bot, response):
        print("ID of successful request: " + response.id)
        bot.send_message("Successfully moved to target coordinates")

    def on_error(self, bot, response):
        print("ID of failed request: " + response.id)
        print("Reason(s) for failure: " + str(response.errors))
        bot.send_message("Failed to move to target coordinates")


def go_home():
    token = get_farmbot_token(config.farmbot_email, config.farmbot_password, config.farmbot_url)
    fb = Farmbot(token)
    handler = MoveHome(0, 0, 0)
    fb.connect(handler)
