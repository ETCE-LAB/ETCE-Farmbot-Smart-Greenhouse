from farmbot import Farmbot
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


class WateringOperationsHandler:
    def __init__(self, nozzle_pickup):
        self.nozzle_pickup = nozzle_pickup
        self.is_watering = False
        self.current_x = 200
        self.direction = 1
        self.x_maxValue = 3000
        self.y_maxValue = 1228

    def on_connect(self, bot, mqtt_client):
        bot.move_absolute(*self.nozzle_pickup)
        print("Connected to FarmBot. Moving to pick up the watering nozzle...")

    def on_change(self, bot, state):
        pos = state["location_data"]["position"]
        xyz = (pos["x"], pos["y"], pos["z"])

        # Check if it's the starting position to pick up nozzle
        if xyz == self.nozzle_pickup:
            print("Watering nozzle picked up. Starting watering operations...")
            bot.toggle_pin(pin_number=config.water_valve_pin)
            self.is_watering = True
            bot.move_absolute(x=self.current_x, y=self.y_maxValue, z=0)

        # Perform the S pattern watering
        elif self.is_watering:
            if self.direction == 1 and xyz[1] == self.y_maxValue:
                bot.toggle_pin(pin_number=config.water_valve_pin)  # Turn off water
                self.current_x += 200
                self.direction = -1
                if self.current_x > self.x_maxValue:
                    bot.move_absolute(*self.nozzle_pickup)
                    self.is_watering = False
                else:
                    bot.move_absolute(x=self.current_x, y=self.y_maxValue, z=0)
                    bot.toggle_pin(pin_number=config.water_valve_pin)  # Turn on water
                    bot.move_absolute(x=self.current_x, y=0, z=0)

            elif self.direction == -1 and xyz[1] == 0:
                bot.toggle_pin(pin_number=config.water_valve_pin)  # Turn off water
                self.current_x += 200
                self.direction = 1
                if self.current_x > self.x_maxValue:
                    bot.move_absolute(*self.nozzle_pickup)  # Return to nozzle pickup position
                    self.is_watering = False
                else:
                    bot.move_absolute(x=self.current_x, y=0, z=0)
                    bot.toggle_pin(pin_number=config.water_valve_pin)
                    bot.move_absolute(x=self.current_x, y=self.y_maxValue, z=0)

        if not self.is_watering and xyz == self.nozzle_pickup:
            print("Watering completed. Returning to home position...")
            bot.move_absolute(x=0, y=0, z=0)  # Move to home position

    def on_log(self, bot, log):
        print("FarmBot: " + log['message'])

    def on_response(self, bot, response):
        print("Successful request ID: " + response.id)

    def on_error(self, bot, response):
        print("Failed request ID: " + response.id + ", Reason: " + str(response.errors))


def execute_watering_sequence():
    token = get_farmbot_token(config.farmbot_email, config.farmbot_password, config.farmbot_url)
    fb = Farmbot(token)
    handler = WateringOperationsHandler(nozzle_pickup=(9, 1074, -410))
    fb.connect(handler)
