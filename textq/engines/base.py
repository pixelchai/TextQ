from abc import abstractmethod
from typing import Iterable
from .. import model

class BaseEngine(model.Hashable):
    @abstractmethod
    def run(self, im) -> Iterable[model.Region]:
        pass

    def compute_hash(self) -> str:
        return type(self).__name__