from app import app, db
from Scheduler.WaterMonitorScheduler import scheduler_service as water_monitor_scheduler_service
from Scheduler.WeatherStationScheduler import scheduler_service as weather_station_scheduler_service
from Scheduler.WeatherPredictionScheduler import scheduler_service as weather_prediction_scheduler_service


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_tables()
    water_monitor_scheduler_service.start()
    weather_station_scheduler_service.start()
    weather_prediction_scheduler_service.start()
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
