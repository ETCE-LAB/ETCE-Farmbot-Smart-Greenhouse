from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()

    def add_job(self, func, trigger, **kwargs):
        self.scheduler.add_job(func, trigger, **kwargs)