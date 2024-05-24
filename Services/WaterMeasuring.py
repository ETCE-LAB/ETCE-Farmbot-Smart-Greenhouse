import RPi.GPIO as GPIO
import time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


def measure_distance():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    TRIG = 23
    ECHO = 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("Distance:", distance, "cm")
    return distance


def calculate_and_store_volume(db, WaterManagementData):
    try:
        distance = measure_distance()
        height = 78
        length = 73
        width = 54
        volume = (height - distance) * length * width

        new_data = WaterManagementData(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            volume=round(volume, 1) / 1000 ,
            fetched_at=datetime.utcnow()
        )
        db.session.add(new_data)
        db.session.commit()
        print("Data stored in database")
    except Exception as e:
        print(f"Error storing data: {str(e)}")
    finally:
        GPIO.cleanup()
