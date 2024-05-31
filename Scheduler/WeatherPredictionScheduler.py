from Scheduler.SchedulerClass import SchedulerService
from Services.WeatherPredictionService import fetch_weather_forecast_range
import datetime

scheduler_service = SchedulerService()

start_date = datetime.datetime.now().strftime('%Y-%m-%d')
end_date = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d')
scheduler_service.add_job(fetch_weather_forecast_range, 'interval', hours=8, args=[start_date, end_date])
