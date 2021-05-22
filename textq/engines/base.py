from abc import abstractmethod
from typing import Iterable
from .. import model

class BaseEngine:
    @abstractmethod
    def run(self, im) -> Iterable[model.Region]:
        pass