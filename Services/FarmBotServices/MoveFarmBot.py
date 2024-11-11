from urllib.error import HTTPError
from farmbot import Farmbot
import config

def move_to(x, y, z):
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
        fb.move(x=x,y=y,z=-z)
    except KeyboardInterrupt:
        return {
            'status': 'FarmBot has reached the target coordinates',
            'x': x,
            'y': y,
            'z': z,
        }
