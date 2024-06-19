import time
from datetime import datetime
from DataLayer import WaterManagementRepository
from DataLayer.Models.WaterManagementModel import WaterManagementData
from Services.IWaterManagementService import IWaterManagementService


def is_raspberry_pi():
    try:
        with open('/proc/device-tree/model') as f:
            model = f.read().lower()
            return 'raspberry pi' in model
    except Exception:
        return False


if is_raspberry_pi():
    import RPi.GPIO as GPIO
else:
    GPIO = None  # Define GPIO as None to prevent errors in non-Raspberry Pi environments


class WaterManagementService(IWaterManagementService):

    def measure_and_store_volume(self):
        if not is_raspberry_pi():
            print(
                datetime.now().strftime('%d-%m %H:%M') + " Not running on a Raspberry Pi, can't measure water volume.")
            return
        else:
            try:
                # Measure distance
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                trigger = 23
                echo = 24
                GPIO.setup(trigger, GPIO.OUT)
                GPIO.setup(echo, GPIO.IN)
                GPIO.output(trigger, False)
                print("Waiting For Sensor To Settle")
                time.sleep(2)
                GPIO.output(trigger, True)
                time.sleep(0.00001)
                GPIO.output(trigger, False)
                while GPIO.input(echo) == 0:
                    pulse_start = time.time()
                while GPIO.input(echo) == 1:
                    pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance, 2)
                print("Distance:", distance, "cm")

                if distance is None:
                    return

                # Calculate and store volume
                height = 78
                length = 73
                width = 54
                volume = (height - distance) * length * width

                new_data = WaterManagementData(
                    date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                    volume=int(round(volume / 1000)),
                    fetched_at=datetime.utcnow()
                )

                WaterManagementRepository.add_water_data(new_data)
                print(datetime.now().strftime('%d-%m %H:%M') + " Water measurement successful, data saved.")
            except Exception as e:
                print(f"Error storing volume data: {str(e)}")
            finally:
                GPIO.cleanup()

    @staticmethod
    def get_all_water_data():
        return WaterManagementRepository.get_all_water_data()

    @staticmethod
    def get_last_water_data():
        return WaterManagementRepository.get_last_water_data()

    @staticmethod
    def get_volume_by_date(date):
        return WaterManagementRepository.get_volume_by_date(date)

    @staticmethod
    def get_volume_by_date_range(start_date, end_date):
        return WaterManagementRepository.get_volume_by_date_range(start_date, end_date)
