
from abc import ABC, abstractmethod

class MiruPlugin(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def icon(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def run(self, context):
        """
        Ejecuta la acción del plugin.
        context: Objeto que provee acceso a la UI y servicios del core (e.g. DeviceManager, Logger).
        """
        pass
