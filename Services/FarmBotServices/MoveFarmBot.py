from urllib.error import HTTPError
from farmbot import Farmbot
import config

def move_to(x, y, z):
    email = config.farmbot_email
    password = config.farmbot_password
    url = config.farmbot_url
    fb = Farmbot()
    token=fb.get_token(email,password,url)
    fb.set_token(token)
    try:
        fb.move(x=x,y=y,z=-z)
    except KeyboardInterrupt:
        return {
            'status': 'FarmBot has reached the target coordinates',
            'x': x,
            'y': y,
            'z': z,
        }
