from app import app, db
from Scheduler.scheduler import scheduler


def create_tables():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_tables()
    scheduler.start()
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
