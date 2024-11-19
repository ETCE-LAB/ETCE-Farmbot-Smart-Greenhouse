from Scheduler.SchedulerClass import SchedulerService
from Services.GreenHouseService import GreenHouseService

Green_house_service=GreenHouseService()

scheduler_service = SchedulerService()

# below scheduler run the service from greenhouse service
# adding scheduler to run humidity and temperature measurment 
scheduler_service.add_job(Green_house_service.measure_temp_humidity, 'interval', minutes=1)  

# adding scheduler to run soil moisture measurment 
scheduler_service.add_job(Green_house_service.measure_soil_moisture, 'interval', hours=8)  # run every hour
