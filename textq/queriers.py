from typing import Optional, List
import segmenters
import readers
import model

class TextQuerier:
    def __init__(self, image, segmenter: segmenters.BaseSegmenter, reader: Optional[readers.BaseReader] = None):
        self.image = image

        self.__segmenter = segmenter
        self.__reader = reader

        self.__segments: List[model.Segment] = []