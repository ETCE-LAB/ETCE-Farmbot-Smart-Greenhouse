from apscheduler.schedulers.background import BackgroundScheduler

from Services.WaterMeasuring import calculate_and_store_volume
from Services.WeatherPredictionService import fetch_weather_forecast_range
from Services.WeatherStationService import fetch_and_process_data

import datetime

scheduler = BackgroundScheduler()

scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)
scheduler.add_job(fetch_weather_forecast_range, 'interval', hours=8, args=[(datetime.datetime.now()).strftime('%Y-%m-%d'), (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d')])
scheduler.add_job(calculate_and_store_volume, 'interval', hours=24)
# TODO: remove forecast from here and make it work in a separate scheduler
