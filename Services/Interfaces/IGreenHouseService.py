from abc import ABC, abstractmethod

class IGreenHouseService(ABC):

    @abstractmethod
    def measure_soil_moisture(self):
        pass