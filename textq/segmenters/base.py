from abc import abstractmethod
from typing import Iterable
from .. import model

class BaseSegmenter:
    @abstractmethod
    def segment(self, im) -> Iterable[model.Segment]:
        pass