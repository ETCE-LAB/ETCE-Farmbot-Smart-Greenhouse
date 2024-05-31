from Scheduler.SchedulerClass import SchedulerService
from Services.WaterMeasuringService import is_raspberry_pi, calculate_and_store_volume
from app import db

scheduler_service = SchedulerService()


if is_raspberry_pi():
    scheduler_service.add_job(calculate_and_store_volume, 'interval', hours=8)
