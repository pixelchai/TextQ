from typing import Optional

class Rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Segment:
    def __init__(self, rect: Rect, text: Optional[str] = None):
        self.rect = rect
        self.text = text
