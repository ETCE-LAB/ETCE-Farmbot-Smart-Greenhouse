from Scheduler.SchedulerClass import SchedulerService
from Services.WaterManagementService import WaterManagementService

water_management_service = WaterManagementService()

scheduler_service = SchedulerService()

scheduler_service.add_job(water_management_service.measure_and_store_volume, 'interval', hours=8)  # run 3 times a day
