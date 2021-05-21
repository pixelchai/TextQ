from abc import abstractmethod
from typing import List
from .. import model

class BaseSegmenter:
    @abstractmethod
    def segment(self, im) -> List[model.Segment]:
        pass