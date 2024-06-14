import time
from datetime import datetime
from DataLayer import GreenHouseRepository
from DataLayer.Models.GreenHouseModel import GreenHouseData


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


def measure_and_store_data():
    if not is_raspberry_pi():
        print(datetime.now().strftime(
            '%d-%m %H:%M') + " Not running on a Raspberry Pi, can't measure temperature and humidity.")
        return

    try:
        # Initialize the DHT22 sensor
        sensor = adafruit_dht.DHT22(board.D4)

        # Read temperature and humidity
        temperature_c = sensor.temperature
        humidity = sensor.humidity
        print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature_c, humidity))

        # Create a new data entry
        new_data = GreenHouseData(
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            temperature=temperature_c,
            humidity=humidity,
            fetched_at=datetime.utcnow()
        )
        print(new_data)

        # Store the data in the repository
        GreenHouseRepository.add_greenhouse_data(new_data)
        print(datetime.now().strftime('%d-%m %H:%M') + " Temperature and humidity measurement successful, data saved.")
    except RuntimeError as error:
        print("Runtime error:", error.args[0])
    except Exception as e:
        print(f"Error storing temperature and humidity data: {str(e)}")
    finally:
        # Clean up the sensor
        if is_raspberry_pi():
            sensor.exit()

