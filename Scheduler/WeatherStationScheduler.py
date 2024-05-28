from apscheduler.schedulers.background import BackgroundScheduler
from Services.WeatherStationService import fetch_and_process_data


from farmbot_commands.measure_soil_sequence import execute_measurement_sequence

scheduler = BackgroundScheduler()

scheduler.add_job(fetch_and_process_data, 'interval', minutes=15)
scheduler.add_job(execute_measurement_sequence, 'interval', hours=12)
# !DONE! TODO: remove forecast from here and make it work in a separate scheduler
