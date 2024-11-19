from urllib.error import HTTPError
from farmbot import Farmbot
import config

def move_to(x, y, z):
    connected = False
    while not connected:
        # get credential from config.py file
        email = config.farmbot_email
        password = config.farmbot_password
        url = config.farmbot_url
        try:
            # connecting to farmbot web service needs to generate toekn, with the new farmbot 2.0.5 library it generates as below and get connected
            fb = Farmbot()
            token=fb.get_token(email,password,url)
            fb.set_token(token)
            connected = True
        except Exception as e:
            print('Token Exception: ', e)
            connected = False
    try:
        # using function from new library, as the z value is defined to be positive in the defined web app, here we make it minus to work o farmbot
        fb.move(x=x,y=y,z=-z)
    except KeyboardInterrupt:
        return {
            'status': 'FarmBot has reached the target coordinates',
            'x': x,
            'y': y,
            'z': z,
        }
