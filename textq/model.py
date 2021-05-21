from typing import Optional, List, Tuple

class Segment:
    def __init__(self, polygon: List[Tuple], text: Optional[str] = None):
        self.polygon = polygon
        self.text = text
