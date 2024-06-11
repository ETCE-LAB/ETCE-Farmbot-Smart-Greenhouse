from abc import ABC, abstractmethod


class IWeatherPredictionService(ABC):

    @abstractmethod
    def fetch_weather_forecast(self, date):
        pass

    @abstractmethod
    def fetch_weather_forecast_range(self, start_date, end_date):
        pass

    @abstractmethod
    def get_weather_forecast_by_date(self, date):
        pass
