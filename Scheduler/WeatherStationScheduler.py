from apscheduler.schedulers.background import BackgroundScheduler
from Services.services import fetch_and_process_data, fetch_weather_forecast, fetch_weather_forecast_range
import datetime

scheduler = BackgroundScheduler()

scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)