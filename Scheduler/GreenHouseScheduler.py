from Scheduler.SchedulerClass import SchedulerService
from Services import GreenHouseService


scheduler_service = SchedulerService()

scheduler_service.add_job(GreenHouseService.measure_and_store_data, 'interval', hours=1)  # run every hour
