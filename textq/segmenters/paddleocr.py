from typing import Iterable
from .base import BaseSegmenter
from .. import model
from paddleocr import PaddleOCR
import cv2
import numpy as np

class PaddleOCRSegmenter(BaseSegmenter):
    def __init__(self, paddle_ocr=None, rec=True):
        if paddle_ocr is None:
            paddle_ocr = PaddleOCR(use_angle_cls=False, lang='en')

        self.__ocr = paddle_ocr
        self.rec = rec

    def segment(self, im) -> Iterable[model.Segment]:
        opencv_im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        result = self.__ocr.ocr(opencv_im, cls=False, rec=self.rec)

        for line in result:
            if self.rec:
                yield model.Segment(line[0], *line[1])
            else:
                yield model.Segment(line[0])
