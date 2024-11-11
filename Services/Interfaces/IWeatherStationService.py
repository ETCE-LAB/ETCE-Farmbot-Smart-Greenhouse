from abc import ABC, abstractmethod

class IWeatherStationService(ABC):

    @abstractmethod
    def fetch_weather_station_data(self):
        pass

    @abstractmethod
    def handle_partial_json(self, text):
        pass

    @abstractmethod
    def fetch_weather_data_by_date(self, date_str):
        pass

    @abstractmethod
    def fetch_weather_data_by_date_range(self, start_date_str, end_date_str):
        pass