import time
from datetime import datetime
from DataLayer import GreenHouseRepository
from DataLayer.Models.GreenHouseModel import GreenHouseData
from Services.FarmBotServices import MeasureSoilMoisture
from Services.Interfaces.IGreenHouseService import IGreenHouseService
from DataLayer.GreenHouseRepository import add_greenhouse_data
from app import app
import requests


# if measurment of temp and humi was set on the same raspberry, then the below function is capable to do measure 

# def is_raspberry_pi():
#     try:
#         with open('/proc/device-tree/model') as f:
#             model = f.read().lower()
#             return 'raspberry pi' in model
#     except Exception:
#         return False


# if measurment of temp and humi was set on the same raspberry, then the below function is capable to do measure 

# if is_raspberry_pi():
#     import board
#     import adafruit_dht
# else:
#     board = None
#     adafruit_dht = None

class GreenHouseService(IGreenHouseService):
    def measure_soil_moisture(self):
        with app.app_context():
            MeasureSoilMoisture.measure_soil_moisture_sequence()
    def measure_temp_humidity(self):
        with app.app_context():
            measure_temperature_humidity()

def measure_temperature_humidity():
    url = "http://172.20.10.11"  ###replace it by pico IP
    for i in range(3):
        try:
            response=requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(data)
                temp=data["temp"]
                humi=data["humi"]
                print('temperature: ',temp)
                print('humidity: ',humi)
                Greenhouse_Data=GreenHouseData( date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),sensor='DHT22',cordinates="Mounted in Greenhouse",temperature=float(temp),humidity=float(humi),soilmoisture=float(0.0))
                add_greenhouse_data(Greenhouse_Data)
                break
            else:
                print('failed to get temperature humidity response')
        except requests.exceptions.RequestException as e:
            print('connection to temperature humidity pico-w error:', e)
            time.sleep(1)

# if measurment of temp and humi was set on the same raspberry, then the below function is capable to do measure 

# def measure_and_store_data():
#     if not is_raspberry_pi():
#         print(datetime.now().strftime(
#             '%d-%m %H:%M') + " Not running on a Raspberry Pi, can't measure temperature and humidity.")
#         return

#     try:
#         # Initialize the DHT22 sensor
#         sensor = adafruit_dht.DHT22(board.D4)

#         # Read temperature and humidity
#         temperature_c = sensor.temperature
#         humidity = sensor.humidity
#         print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature_c, humidity))

#         # Create a new data entry
#         new_data = GreenHouseData(
#             date=datetime.now().strftime("%Y-%m-%d %H:%M"),
#             temperature=temperature_c,
#             humidity=humidity,
#             fetched_at=datetime.utcnow()
#         )
#         print(new_data)
#         GreenHouseRepository.add_greenhouse_data(new_data)
#         print(datetime.now().strftime('%d-%m %H:%M') + " Temperature and humidity measurement successful, data saved.")
#     except RuntimeError as error:
#         print("Runtime error:", error.args[0])
#     except Exception as e:
#         print(f"Error storing temperature and humidity data: {str(e)}")
#     finally:
#         if is_raspberry_pi():
#             sensor.exit()


def get_all_temperature():
    return GreenHouseRepository.get_all_temperature()


def get_all_humidity():
    return GreenHouseRepository.get_all_humidity()


def get_temperature_by_date(date):
    return GreenHouseRepository.get_temperature_by_date(date)


def get_humidity_by_date(date):
    return GreenHouseRepository.get_humidity_by_date(date)


def get_all_data():
    return GreenHouseRepository.get_all_data()


def get_data_by_date(date):
    return GreenHouseRepository.get_data_by_date(date)


def get_humidity_range(start_date, end_date):
    return GreenHouseRepository.get_humidity_by_date_range(start_date, end_date)


def get_temperature_range(start_date, end_date):
    return GreenHouseRepository.get_temperature_by_date_range(start_date, end_date)
