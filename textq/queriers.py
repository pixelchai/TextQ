from typing import Optional, Tuple
from .engines import BaseEngine
from .correctors import BaseCorrector
from .model import Region, Hashable
from shapely.geometry import Point, box
from shapely.geometry.polygon import Polygon
from PIL import Image
import os
import json

class TextQuerier(Hashable):
    def __init__(self, image,
                 engine: BaseEngine,
                 corrector: BaseCorrector = None,
                 no_newlines=True,
                 cache_dir="cache"):
        self.image = None
        self.set_image(image)

        self.engine = engine
        self.corrector = corrector

        self.no_newlines = no_newlines
        self._cache_dir = cache_dir

        self.regions: Optional[Tuple[Region]] = None

        if not os.path.isdir(self._cache_dir):
            os.makedirs(self._cache_dir)

    def compute_hash(self) -> str:
        return self._combine_hashes(
            self.engine.compute_hash(),
            self._hash_bytes(self.image.resize((100, 100), resample=Image.NEAREST).tobytes())
        )

    def _get_regions(self):
        if self.image is None:
            return

        # load cache
        cache = {}
        cache_path = os.path.join(self._cache_dir, "cache.json")
        if os.path.isfile(cache_path):
            with open(cache_path, "r") as f:
                cache.update(json.load(f))

        cur_hash = self.compute_hash()

        # return from cache if available
        if cur_hash in cache:
            return [Region(**kw) for kw in cache[cur_hash]]

        # was not in cache, so compute regions using engine
        regions = tuple(self.engine.run(self.image))

        # update and save cache
        cache[cur_hash] = [region.__dict__ for region in regions]
        with open(cache_path, "w") as f:
            json.dump(cache, f)

        return regions

    def run(self):
        self.regions = self._get_regions()

    def set_image(self, image):
        self.image = image

        if self.image is not None:
            self.run()

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
