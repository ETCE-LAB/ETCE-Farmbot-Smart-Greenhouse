from Scheduler.SchedulerClass import SchedulerService
from Services.WeatherStationService import WeatherStationService

weather_station_service = WeatherStationService()

scheduler_service = SchedulerService()

scheduler_service.add_job(weather_station_service.fetch_weather_station_data, 'interval', minutes=15)
