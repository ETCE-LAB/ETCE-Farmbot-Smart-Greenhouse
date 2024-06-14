import time
from datetime import datetime
from DataLayer import GreenHouseRepository
from DataLayer.Models.GreenHouseModel import GreenHouseData
from Services.Interfaces.IGreenHouseService import IGreenHouseService


def is_raspberry_pi():
    try:
        with open('/proc/device-tree/model') as f:
            model = f.read().lower()
            return 'raspberry pi' in model
    except Exception:
        return False


if is_raspberry_pi():
    import board
    import adafruit_dht
else:
    board = None
    adafruit_dht = None


class GreenHouseService(IGreenHouseService):

    def measure_and_store_data(self):
        sensor = adafruit_dht.DHT22(board.D4)
        if not is_raspberry_pi():
            print(
                datetime.now().strftime(
                    '%d-%m %H:%M') + " Not running on a Raspberry Pi, can't measure temperature and humidity.")
            return
        else:
            try:
                temperature_c = sensor.temperature
                humidity = sensor.humidity
                print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature_c, humidity))

                new_data = GreenHouseData(
                    date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                    temperature=temperature_c,
                    humidity=humidity,
                    fetched_at=datetime.utcnow()
                )
                print(new_data)
                GreenHouseRepository.add_greenhouse_data(new_data)
                print(datetime.now().strftime(
                    '%d-%m %H:%M') + " Temperature and humidity measurement successful, data saved.")
            except RuntimeError as error:
                print(error.args[0])
                sensor.exit()

            except Exception as e:
                print(f"Error storing temperature and humidity data: {str(e)}")
                sensor.exit()
                raise e

    @classmethod
    def get_all_humidity(cls):
        return GreenHouseRepository.get_all_humidity()

    @classmethod
    def get_everything(cls):
        return cls.measure_and_store_data()

    @classmethod
    def get_all_temperature(cls):
        return GreenHouseRepository.get_all_temperature()

    @classmethod
    def get_last_temperature(cls):
        return GreenHouseRepository.get_last_temperature()

    @classmethod
    def get_last_humidity(cls):
        return GreenHouseRepository.get_last_humidity()

    @classmethod
    def get_temperature_by_date(cls, date):
        return GreenHouseRepository.get_temperature_by_date(date)

    @classmethod
    def get_humidity_by_date(cls, date):
        return GreenHouseRepository.get_humidity_by_date(date)