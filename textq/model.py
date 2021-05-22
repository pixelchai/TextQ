from typing import Optional, Iterable, Tuple

class Segment:
    def __init__(self, polygon: Iterable[Tuple], text: Optional[str] = None, confidence: Optional[float] = 1.0):
        self.polygon = polygon
        self.text = text
        self.confidence = confidence

    def __repr__(self):
        return "<" + \
               "[" + ", ".join(("(" + ", ".join(map(str, vertex)) + ")" for vertex in self.polygon)) + "]" + \
               ', "{}" '.format(self.text) + \
               ", {:.02f}".format(self.confidence) + \
               ">"