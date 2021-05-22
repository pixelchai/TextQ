from typing import Optional, List, Tuple
from . import engines
from . import model

class TextQuerier:
    def __init__(self, image, engine: engines.BaseEngine):
        self.image = image

        self.engine = engine
        self.regions: Optional[Tuple[model.Region]] = None

    def run(self):
        self.regions = tuple(self.engine.run(self.image))
        print(self.regions)