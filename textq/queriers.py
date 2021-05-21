from typing import Optional, List, Tuple
from . import segmenters
from . import readers
from . import model

class TextQuerier:
    def __init__(self, image, segmenter: segmenters.BaseSegmenter, reader: Optional[readers.BaseReader] = None):
        self.image = image

        self.__segmenter = segmenter
        self.__reader = reader

        self.__segments: Optional[Tuple[model.Segment]] = None

    def segment(self):
        self.__segments = tuple(self.__segmenter.segment(self.image))
        print(self.__segments)