import textq
import time
from PIL import Image, ImageDraw, ImageFont

im_path = "/home/ab/mrtest/negexamples/006.jpg"
im = Image.open(im_path)

from textq.engines.paddleocr_engine import PaddleOCREngine as Engine
q = textq.TextQuerier(im, Engine())

time_initial = time.time()
q.run()
print("Took: {}s".format(time.time() - time_initial))

# draw debug info
draw = ImageDraw.Draw(im)
font = ImageFont.truetype("res/OpenSans.ttf", size=20)
for region in q.regions:
    poly = list(map(tuple, region.polygon))
    draw.polygon(poly, outline=(255, 0, 0))

    mid = tuple(map(lambda x: x/len(poly), [sum(l) for l in zip(*poly)]))
    draw.text(mid, f"{region.text} [{region.confidence:.02f}]", font=font, fill=(255, 0, 0), align='center')

im.show()

# import textq
# c = textq.correctors.DuckDuckGoCorrector()
# corrected = c.correct("ranltithe greatest villain of all time")
# print(corrected)