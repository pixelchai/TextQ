import re
from typing import Optional, List, Tuple
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
        self.image = image

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

        # load index
        # NB: using index because some systems have restrictions on file name length
        index = {}
        index_path = os.path.join(self._cache_dir, "index.json")
        if os.path.isfile(index_path):
            with open(index_path, "r") as f:
                index.update(json.load(f))

        cur_hash = self.compute_hash()

        # return from cache if available
        if cur_hash in index:
            cache_path = os.path.join(self._cache_dir, os.path.normpath(index[cur_hash]))

            if os.path.isfile(cache_path):
                with open(cache_path, "r") as f:
                    return [Region(**kw) for kw in json.load(f)]
            else:
                index.pop(cur_hash)

        # was not in cache, so compute regions using engine
        regions = tuple(self.engine.run(self.image))

        def int_to_string(num):
            alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
            if num == 0:
                return ""
            else:
                return int_to_string(num // len(alphabet)) + alphabet[num % len(alphabet)]

        # save regions to cache
        rel_cache_path = int_to_string(len(os.listdir(self._cache_dir)) + 1) + ".json"
        with open(os.path.join(self._cache_dir, rel_cache_path), "w") as f:
            json.dump([region.__dict__ for region in regions], f)

        # update and save index
        index[cur_hash] = rel_cache_path
        with open(index_path, "w") as f:
            json.dump(index, f)

        return regions

    def run(self):
        self.regions = self._get_regions()

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
