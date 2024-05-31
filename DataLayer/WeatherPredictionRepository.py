from app import db


def add_forecast(forecast):
    db.session.add(forecast)
    db.session.commit()


def add_forecasts(forecasts):
    for forecast in forecasts:
        db.session.add(forecast)
    db.session.commit()

def get_forecast(id):
    # find by id

def get_all_forecasts():
    # query all

def update_forecast(id, forecast):
    # update forecast of id with value
    # from forecast input

def delete_forecast(id):
    #delete forcast where id = id
        
