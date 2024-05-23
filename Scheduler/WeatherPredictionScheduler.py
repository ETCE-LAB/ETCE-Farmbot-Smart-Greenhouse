"""
from apscheduler.schedulers.background import BackgroundScheduler
from Services.WeatherPredictionService import fetch_weather_forecast_range
import datetime

scheduler = BackgroundScheduler()

scheduler.add_job(fetch_weather_forecast_range, 'interval', seconds=10, args=[(datetime.datetime.now()).strftime('%Y-%m-%d'), (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d')])
"""