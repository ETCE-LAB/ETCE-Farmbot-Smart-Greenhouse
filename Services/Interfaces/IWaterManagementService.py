from abc import ABC, abstractmethod


class IWaterManagementService(ABC):

    @abstractmethod
    def measure_and_store_volume(self):
        pass
