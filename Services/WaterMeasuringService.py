import time
from datetime import datetime
import RPi.GPIO as GPIO


def measure_distance():
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


def calculate_and_store_volume(db, water_management_data):
    try:
        distance = measure_distance()
        height = 78
        length = 73
        width = 54
        volume = (height - distance) * length * width

        new_data = water_management_data(
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            volume=int(round(volume / 1000)),
            fetched_at=datetime.utcnow()
        )
        db.session.add(new_data)
        db.session.commit()
        print("Data stored in database")
    except Exception as e:
        print(f"Error storing data: {str(e)}")
    finally:
        GPIO.cleanup()
