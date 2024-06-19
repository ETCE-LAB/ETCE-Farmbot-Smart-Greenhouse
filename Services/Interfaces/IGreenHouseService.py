from abc import ABC, abstractmethod


class IGreenHouseService(ABC):

    @abstractmethod
    def measure_and_store_data(self):
        pass
