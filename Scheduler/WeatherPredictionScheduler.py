from Scheduler.SchedulerClass import SchedulerService
from Services.WeatherPredictionService import WeatherPredictionService
import datetime

scheduler_service = SchedulerService()

start_date = datetime.datetime.now().strftime('%Y-%m-%d')  # today
end_date = (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d')  # today + 15 days
scheduler_service.add_job(
    WeatherPredictionService.fetch_weather_forecast_range,
    'interval',
    hours=8,  # run 3 times a day
    args=[start_date, end_date]
)
