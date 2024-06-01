from Scheduler.SchedulerClass import SchedulerService
from Services.WeatherStationService import fetch_weather_station_data

scheduler_service = SchedulerService()

scheduler_service.add_job(fetch_weather_station_data, 'interval', minutes=15)
