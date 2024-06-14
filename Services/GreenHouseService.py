import time
from datetime import datetime
from DataLayer import GreenHouseRepository
from DataLayer.Models.GreenHouseModel import GreenHouseData
from Services.Interfaces.IGreenHouseService import IGreenHouseService
import board
import adafruit_dht

class GreenHouseService(IGreenHouseService):

    def __init__(self):
        print("Initializing GreenHouseService")
        self.sensor = adafruit_dht.DHT22(board.D4)

    def measure_and_store_data(self):
        print("measure_and_store_data called")
        try:
            temperature_c = self.sensor.temperature
            humidity = self.sensor.humidity
            print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature_c, humidity))

            new_data = GreenHouseData(
                date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                temperature=temperature_c,
                humidity=humidity,
                fetched_at=datetime.utcnow()
            )
            print(new_data)
            GreenHouseRepository.add_greenhouse_data(new_data)
            print(datetime.now().strftime('%d-%m %H:%M') + " Temperature and humidity measurement successful, data saved.")
        except RuntimeError as error:
            print("Runtime error:", error.args[0])
        except Exception as e:
            print(f"Error storing temperature and humidity data: {str(e)}")
            self.sensor.exit()
            raise e

    def get_all_humidity(self):
        return GreenHouseRepository.get_all_humidity()

    def get_all_temperature(self):
        return GreenHouseRepository.get_all_temperature()

    def get_last_temperature(self):
        return GreenHouseRepository.get_last_temperature()

    def get_last_humidity(self):
        return GreenHouseRepository.get_last_humidity()

    def get_temperature_by_date(self, date):
        return GreenHouseRepository.get_temperature_by_date(date)

    def get_humidity_by_date(self, date):
        return GreenHouseRepository.get_humidity_by_date(date)


