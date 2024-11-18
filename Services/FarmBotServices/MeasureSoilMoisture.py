from farmbot import Farmbot
import time
from urllib.error import HTTPError
import config
from Services.FarmBotServices.MoveFarmBot import move_to
from DataLayer.Models.GreenHouseModel import GreenHouseData
from DataLayer.GreenHouseRepository import add_greenhouse_data
import json
import requests
from app import app

    

def measure_soil_moisture_sequence():
    with app.app_context():
        connected = False
        while not connected:
            email = config.farmbot_email
            password = config.farmbot_password
            url = config.farmbot_url
            try:
                fb = Farmbot()
                token=fb.get_token(email,password,url)
                fb.set_token(token)
                connected = True
            except Exception as e:
                print('Token Exception: ', e)
                connected = False

        try:
            fb.on(7) # turn on bot led light
            move_to(1,1,0)
            move_to(15,83,0)
            move_to(15,83,414)
            move_to(100,83,414)
            move_to(100,83,0)
            move_to(1600,400,0)
            move_to(1600,400,500)
            fb.read_sensor('Soil Sensor')
            time.sleep(2) # needs sometime to read
            # start of reading data from farmbot
            

            ## incase for manual data insertion into sqlite3 use below commented codes
            # db_path = os.path.join('/home/rpi/ETCE-Farmbot-Smart-Greenhouse/instance', 'smart_greenhouse.db')  # Use a relative path
            # conn=sqlite3.connect(db_path)
            # cursor = conn.cursor()
            # sql_insert = """INSERT INTO farm_bot_data (measurement, value, pin, x_position, y_position, z_position, read_at, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
            # # Step 3: Define the values to insert
            # values = ('soil_moisture',latest_value, 59, x_po, y_po, z_po, latest_read_at, latest_created_at)  # Replace with actual values
            # try:
            #     # Step 4: Execute the command
            #     cursor.execute(sql_insert, values)
            #     # Step 5: Commit the transaction
            #     conn.commit()
            #     print("Data inserted successfully.")
            # except sqlite3.Error as e:
            #     print("An error occurred:", e)
            # fb.on(7)

            move_to(1600,400,0)
            move_to(100,83,0)
            move_to(100,83,414)
            move_to(15,83,414)
            move_to(15,83,0)
            move_to(1,1,0)
            fb.off(7) # turn off led
        finally:
            print("Measurement sequence completed.")
        
        try:
            url_read = f'https://my.farm.bot:443/api/sensor_readings'
            headers = {'Authorization': 'Bearer ' + token['token']['encoded'],'content-type': 'application/json'}
            response = requests.get(url_read, headers=headers)
            sensor_data = response.json()
            pin_59_readings = [entry for entry in sensor_data if entry['pin'] == 59]
            # Sort the filtered readings by 'read_at' in descending order to get the latest reading first
            latest_reading = sorted(pin_59_readings, key=lambda x: x['read_at'], reverse=True)[0]
            # print(latest_reading)
            # Extract value, created_at, and read_at into separate variables
            latest_value = latest_reading['value']
            latest_created_at = latest_reading['created_at']
            latest_read_at = latest_reading['read_at']
            pin= latest_reading['pin']
            x_po = latest_reading['x']
            y_po = latest_reading['y']
            z_po = latest_reading['z']
            Soil_Moisture_Data=GreenHouseData( date=latest_read_at,sensor='Soil Moisture',cordinates=f"{x_po}{','}{y_po}{','}{z_po}",temperature=float(0.0),humidity=(0.0),soilmoisture=float(latest_value))
            # print(Soil_Moisture_Data)

            add_greenhouse_data(Soil_Moisture_Data)
        except Exception as e:
            print('Soil moisture data record Exception: ', e)


if __name__ == "__main__":
    measure_soil_moisture_sequence()
