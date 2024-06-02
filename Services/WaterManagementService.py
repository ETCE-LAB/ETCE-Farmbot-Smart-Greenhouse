import time
from datetime import datetime
from DataLayer.WaterManagementRepository import add_water_data


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


def measure_distance():
    if not is_raspberry_pi():
        print("Not running on a Raspberry Pi. Exiting measure_distance.")
        return None
    else:
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
        return distance


def calculate_and_store_volume():
    if not is_raspberry_pi():
        print(datetime.now().strftime('%d-%m %H:%M') + " Not running on a Raspberry Pi, cant measure water volume.")
        return
    else:
        try:
            distance = measure_distance()
            if distance is None:
                return

            height = 78
            length = 73
            width = 54
            volume = (height - distance) * length * width

            add_water_data(volume)
            print(datetime.now().strftime('%d-%m %H:%M') + " Water measurement successful, data saved.")
        except Exception as e:
            print(f"Error storing volume data: {str(e)}")
        finally:
            GPIO.cleanup()