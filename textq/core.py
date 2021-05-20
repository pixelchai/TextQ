from typing import Optional
import segmenters
import readers

class TextQuerier:
    def __init__(self, image, segmenter: segmenters.BaseSegmenter, reader: Optional[readers.BaseReader] = None):
        self.image = image

        self.__segmenter = segmenter
        self.__reader = reader

class Segment:
    def __init__(self, mask, text=None):
        self.mask = mask
        self.text = text