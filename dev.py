import textq
from textq.engines.paddleocr_engine import PaddleOCREngine as Engine
from textq.correctors.wordsplitting import WordNinjaCorrector as Corrector
from textq import demo
from qtpy import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")

    querier = textq.TextQuerier(None, Engine(), Corrector())

    window = demo.DemoWindow(querier)
    window.show()

    app.exec_()
