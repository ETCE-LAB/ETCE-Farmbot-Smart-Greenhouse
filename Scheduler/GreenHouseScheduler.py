from Scheduler.SchedulerClass import SchedulerService
from Services.GreenHouseService import GreenHouseService

Green_house_service=GreenHouseService()

scheduler_service = SchedulerService()

scheduler_service.add_job(Green_house_service.measure_soil_moisture, 'interval', minutes=30)  # run every hour
