from typing import Iterable
from .base import BaseEngine
from .. import model
from paddleocr import PaddleOCR
import cv2
import numpy as np

class PaddleOCREngine(BaseEngine):
    def __init__(self, paddle_ocr=None, rec=True):
        if paddle_ocr is None:
            paddle_ocr = PaddleOCR(use_angle_cls=False, lang='en')

        self.__ocr = paddle_ocr
        self.rec = rec

    def run(self, im) -> Iterable[model.Region]:
        opencv_im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        result = self.__ocr.ocr(opencv_im, cls=False, rec=self.rec)

        for line in result:
            polygon = tuple(tuple(map(float, vertex)) for vertex in line[0])
            if self.rec:
                yield model.Region(polygon, str(line[1][0]), float(line[1][1]))
            else:
                yield model.Region(polygon)
