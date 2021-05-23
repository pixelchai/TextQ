from typing import Tuple
from qtpy import QtGui, QtCore
from qtpy.QtCore import Qt
from qtpy.QtWidgets import *
from .canvas import CanvasWidget

class DemoWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
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
        self.top_panel_layout.addWidget(self.edit_path)

        self.btn_load = QPushButton(self.top_panel, text="Load")
        self.top_panel_layout.addWidget(self.btn_load)

        self.layout.addWidget(self.top_panel)
        # endregion

        self.canvas = CanvasWidget(self.central_widget)
        self.layout.addWidget(self.canvas)

        self.setCentralWidget(self.central_widget)
