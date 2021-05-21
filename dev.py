# import textq
# from PIL import Image
#
# im = Image.open("res/test.jpg")
# q = textq.TextQuerier(im, textq.segmenters.PaddleOCRSegmenter())

# https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.1/doc/doc_en/whl_en.md#21-use-by-code
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory
img_path = 'PaddleOCR/doc/imgs_en/img_12.jpg'
result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)