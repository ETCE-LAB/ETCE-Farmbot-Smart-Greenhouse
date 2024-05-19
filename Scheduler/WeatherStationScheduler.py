from apscheduler.schedulers.background import BackgroundScheduler
from Services.WeatherStationService import fetch_and_process_data

import datetime

scheduler = BackgroundScheduler()

scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)