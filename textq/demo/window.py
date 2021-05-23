import os
from typing import Tuple
from qtpy import QtGui, QtCore
from qtpy.QtCore import Qt
from qtpy.QtWidgets import *
import textq
from PIL import Image
from PIL.ImageQt import ImageQt
from .canvas import CanvasWidget

class DemoWindow(QMainWindow):
    def __init__(self, querier: textq.TextQuerier, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.querier = querier

        # region layout code
        self.setWindowTitle("TextQ Demo Window")

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Please load in an image")

        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)

        # region top panel
        self.top_panel = QWidget(self.central_widget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_panel.sizePolicy().hasHeightForWidth())
        self.top_panel.setSizePolicy(sizePolicy)
        self.top_panel_layout = QHBoxLayout(self.top_panel)

        self.label_path = QLabel(self.top_panel, text="Image Path: ")
        self.top_panel_layout.addWidget(self.label_path)

        self.edit_path = QLineEdit(self.top_panel)
        self.edit_path.setText("/home/ab/mrtest/negexamples/001.jpg")
        self.top_panel_layout.addWidget(self.edit_path)

        self.btn_load = QPushButton(self.top_panel, text="Load")
        self.top_panel_layout.addWidget(self.btn_load)

        self.layout.addWidget(self.top_panel)
        # endregion

        self.canvas = CanvasWidget(self.central_widget)
        self.layout.addWidget(self.canvas)

        self.setCentralWidget(self.central_widget)
        # endregion

        self.btn_load.clicked.connect(self._btn_load_clicked)

    def _btn_load_clicked(self):
        im_path = os.path.normpath(self.edit_path.text())
        im = Image.open(im_path)
        self.querier.image = Image.open(im_path)
        self.canvas.set_image(ImageQt(im))
        self.status_bar.clearMessage()
        self.querier.run()
        self.canvas.set_regions(self.querier.regions)
