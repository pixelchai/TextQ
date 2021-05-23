from typing import Iterable
import cv2
import numpy as np
import easyocr
from .. import model
from .base import BaseEngine

class EasyOCREngine(BaseEngine):
    def __init__(self, reader=None):
        if reader is None:
            reader = easyocr.Reader(['en'])

        self.__reader = reader

    def run(self, im) -> Iterable[model.Region]:
        opencv_im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        result = self.__reader.readtext(opencv_im)

        for line in result:
            polygon = tuple(tuple(map(float, vertex)) for vertex in line[0])
            yield model.Region(polygon, str(line[1]), float(line[2]))
