from typing import Optional, List, Tuple
from .engines import BaseEngine
from .correctors import BaseCorrector
from .model import Region

class TextQuerier:
    def __init__(self, image, engine: BaseEngine, corrector: BaseCorrector = None):
        self.image = image

        self.engine = engine
        self.corrector = corrector

        self.regions: Optional[Tuple[Region]] = None

    def run(self):
        self.regions = tuple(self.engine.run(self.image))

        if self.corrector is not None:
            for region in self.regions:
                region.text = self.corrector.correct(region.text)
