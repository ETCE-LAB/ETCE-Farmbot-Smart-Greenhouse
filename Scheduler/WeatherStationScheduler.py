from Scheduler.SchedulerClass import SchedulerService
from Services.WeatherStationService import fetch_and_process_data

scheduler_service = SchedulerService()

scheduler_service.add_job(fetch_and_process_data, 'interval', minutes=15)
