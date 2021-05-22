from abc import abstractmethod

class BaseCorrector:
    @abstractmethod
    def correct(self, text: str) -> str:
        pass