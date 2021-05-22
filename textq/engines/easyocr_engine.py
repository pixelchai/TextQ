from typing import Iterable
import easyocr
from .. import model
from .base import BaseEngine

class EasyOCREngine(BaseEngine):
    def __init__(self, reader=None):
        if reader is None:
            reader = easyocr.Reader(['en'])

        self.__reader = reader

    def run(self, im) -> Iterable[model.Region]:
        result = self.__reader.readtext(im)

        for line in result:
            polygon = tuple(tuple(map(float, vertex)) for vertex in line[0])
            yield model.Region(polygon, *line[1:])
