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
    import RPi.GPIO as GPIO
else:
    GPIO = None  # Define GPIO as None to prevent errors in non-Raspberry Pi environments


class GreenHouseService(IGreenHouseService):

    CMD_MEASURE_TEMP = 0x03
    CMD_MEASURE_HUMI = 0x05
    CMD_SOFT_RESET = 0x1E

    DATA_PIN = 4
    SCK_PIN = 17

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DATA_PIN, GPIO.OUT)
        GPIO.setup(self.SCK_PIN, GPIO.OUT)

    def release_data_line(self):
        GPIO.setup(self.DATA_PIN, GPIO.IN)

    def assert_data_line(self):
        GPIO.setup(self.DATA_PIN, GPIO.OUT)
        GPIO.output(self.DATA_PIN, GPIO.LOW)

    def sck_high(self):
        GPIO.output(self.SCK_PIN, GPIO.HIGH)

    def sck_low(self):
        GPIO.output(self.SCK_PIN, GPIO.LOW)

    def reset_sensor(self):
        self.assert_data_line()
        for _ in range(9):
            self.sck_high()
            time.sleep(0.001)
            self.sck_low()
            time.sleep(0.001)
        self.release_data_line()

    def send_command(self, command):
        self.assert_data_line()
        self.sck_high()
        self.sck_low()
        self.release_data_line()
        for i in range(8):
            if command & (1 << (7 - i)):
                GPIO.output(self.DATA_PIN, GPIO.HIGH)
            else:
                GPIO.output(self.DATA_PIN, GPIO.LOW)
            self.sck_high()
            self.sck_low()
        self.sck_high()
        self.release_data_line()
        self.sck_low()
        ack = GPIO.input(self.DATA_PIN)
        self.sck_high()
        self.sck_low()
        return ack

    def read_byte(self):
        byte = 0
        self.release_data_line()
        for i in range(8):
            byte <<= 1
            self.sck_high()
            if GPIO.input(self.DATA_PIN):
                byte |= 0x01
            self.sck_low()
        self.assert_data_line()
        self.sck_high()
        self.sck_low()
        self.release_data_line()
        return byte

    def read_sensor(self, command):
        self.reset_sensor()
        if self.send_command(command):
            raise RuntimeError("Failed to send command to SHT11 sensor")
        while GPIO.input(self.DATA_PIN):
            time.sleep(0.01)
        value = self.read_byte() << 8
        value += self.read_byte()
        return value

    def get_temperature(self):
        raw_temp = self.read_sensor(self.CMD_MEASURE_TEMP)
        temp_celsius = -39.66 + 0.01 * raw_temp
        return temp_celsius

    def get_humidity(self):
        raw_humi = self.read_sensor(self.CMD_MEASURE_HUMI)
        humidity = -2.0468 + 0.0367 * raw_humi - 1.5955e-6 * (raw_humi ** 2)
        return humidity

    def get_sensor_data(self):
        self.init_gpio()
        try:
            temperature = self.get_temperature()
            humidity = self.get_humidity()
            return temperature, humidity
        finally:
            GPIO.cleanup()

    def measure_and_store_data(self):
        if not is_raspberry_pi():
            print(
                datetime.now().strftime('%d-%m %H:%M') + " Not running on a Raspberry Pi, can't measure temperature and humidity.")
            return
        else:
            try:
                temperature, humidity = self.get_sensor_data()
                print(f"Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f} %")

                new_data = GreenHouseData(
                    date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                    temperature=temperature,
                    humidity=humidity,
                    fetched_at=datetime.utcnow()
                )

                GreenHouseRepository.add_greenhouse_data(new_data)
                print(datetime.now().strftime('%d-%m %H:%M') + " Temperature and humidity measurement successful, data saved.")
            except Exception as e:
                print(f"Error storing temperature and humidity data: {str(e)}")
            finally:
                GPIO.cleanup()

    @classmethod
    def get_all_humidity(cls):
        return GreenHouseRepository.get_all_humidity()

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
