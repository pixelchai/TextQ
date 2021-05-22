from typing import Optional, List, Tuple
from . import engines
from . import model

class TextQuerier:
    def __init__(self, image, engine: engines.BaseEngine):
        self.image = image

        self.__engine = engine
        self.__regions: Optional[Tuple[model.Region]] = None

    def run(self):
        self.__regions = tuple(self.__engine.run(self.image))
        print(self.__regions)