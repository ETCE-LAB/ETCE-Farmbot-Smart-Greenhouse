from Scheduler.SchedulerClass import SchedulerService
from Services.GreenHouseService import GreenHouseService

greenhouse_management_service = GreenHouseService()

scheduler_service = SchedulerService()

scheduler_service.add_job(greenhouse_management_service.measure_and_store_data, 'interval', hours=8)  # run 3 times a day
