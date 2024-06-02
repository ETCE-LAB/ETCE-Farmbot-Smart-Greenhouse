from Scheduler.SchedulerClass import SchedulerService
from Services.WaterManagementService import calculate_and_store_volume

scheduler_service = SchedulerService()


scheduler_service.add_job(calculate_and_store_volume, 'interval', hours=8)  # run 3 times a day
