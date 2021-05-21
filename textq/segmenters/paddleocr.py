from .base import BaseSegmenter
from paddleocr import PaddleOCR

class PaddleOCRSegmenter(BaseSegmenter):
    def __init__(self, **kwargs):
        kwargs["lang"] = "en"
        self.__ocr = PaddleOCR(**kwargs)