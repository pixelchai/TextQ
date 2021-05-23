import re
from typing import Optional, List, Tuple
from .engines import BaseEngine
from .correctors import BaseCorrector
from .model import Region
from shapely.geometry import Point, box
from shapely.geometry.polygon import Polygon

class TextQuerier:
    def __init__(self, image, engine: BaseEngine, corrector: BaseCorrector = None, no_newlines=True):
        self.image = image

        self.engine = engine
        self.corrector = corrector
        self.no_newlines = no_newlines

        self.regions: Optional[Tuple[Region]] = None

    def run(self):
        self.regions = tuple(self.engine.run(self.image))

    def _try_correct(self, text) -> str:
        if self.corrector is not None:
            return self.corrector.correct(text)

        return text

    def _postproc_text(self, text) -> str:
        if self.no_newlines:
            text = text.replace("\n", " ")
        return self._try_correct(text)

    def query_point(self, x, y):
        point = Point(x, y)

        for region in self.regions:
            polygon = Polygon(region.polygon)

            if polygon.contains(point):
                return self._postproc_text(region.text)

        return None

    def query_rect(self, x1, y1, x2, y2):
        rect = box(x1, y1, x2, y2)

        text = ""
        for region in self.regions:
            polygon = Polygon(region.polygon)

            if rect.intersects(polygon):
                text += region.text + (" " if self.no_newlines else "\n")

        text = text[:-1]  # strip out final whitespace
        return self._postproc_text(text)
