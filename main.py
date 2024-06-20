from datetime import datetime

from app import app, db
from Scheduler.WaterManagementScheduler import scheduler_service as water_monitor_scheduler_service
from Scheduler.WeatherStationScheduler import scheduler_service as weather_station_scheduler_service
from Scheduler.WeatherPredictionScheduler import scheduler_service as weather_prediction_scheduler_service
from Scheduler.GreenHouseScheduler import scheduler_service as green_house_scheduler_service


def create_tables():
    with app.app_context():
        db.create_all()


def start_scheduler(scheduler_service, name):
    scheduler_service.start()
    print(f"{name} Scheduler started: {datetime.now()}")


if __name__ == '__main__':
    create_tables()

    schedulers = {
        "Water Management": water_monitor_scheduler_service,
        "Weather Station": weather_station_scheduler_service,
        "Weather Prediction": weather_prediction_scheduler_service,
        "Green House": green_house_scheduler_service,
    }

    for name, service in schedulers.items():
        start_scheduler(service, name)

    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
