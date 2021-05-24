# TextQ
A library for extracting text from images, providing a unified interface to several different OCR implementations

```python
from PIL import Image
from textq import TextQuerier
from textq.engines.paddleocr_engine import PaddleOCREngine
from textq.correctors.wordsplitting import WordNinjaCorrector
from textq.demo import DemoWindow

image = Image.open("path/to/image")
querier = TextQuerier(image, PaddleOCREngine(), WordNinjaCorrector())

# visualisation demo window
window = DemoWindow(querier)
window.show()

# query for text within rectangular regions of interest
text = querier.query_rect(x1, y1, x2, y2)
```

The library is designed with minimising the number of calls to the OCR engines in mind.

Rather than querying the OCR engine for each region of interest within an image, the engine is only called once per image. The results are then cached, both to the filesystem and in memory.
Subsequent queries for text within different regions of interest within the image then operate only on the internal cache rather than querying the engine.

This may be useful, for example, in reducing the number of API requests to OCR services which meter the number of requests.
