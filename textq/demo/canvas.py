from typing import Tuple
from qtpy import QtGui, QtCore
from qtpy.QtCore import Qt
from qtpy.QtWidgets import *

class CanvasWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.cur_x = 0
        self.cur_y = 0
        self._draw_cur = False

        self._off_x = 0
        self._off_y = 0
        self._scale = 1

        self._pixmap = None

        self.setMouseTracking(True)  # https://forum.qt.io/post/153698
        self.mouse_down = False
        self._rect_x1 = 0
        self._rect_y1 = 0
        self._rect_x2 = 0
        self._rect_y2 = 0

        self._regions = None

        self.callback_mouse_press = None
        self.callback_mouse_move = None
        self.callback_mouse_release = None

        self.draw_rect_border = True

    def set_image(self, qim):
        self._pixmap = QtGui.QPixmap.fromImage(qim.copy())
        self._recalc_im()

    @staticmethod
    def _calc_smart_centre(w, h, cw, ch):
        """
        :param w: image width
        :param h: image height
        :param cw: total canvas width
        :param ch: total canvas height
        :param padding_max: max padding value
        :param alpha: if min(cw, ch) -> alpha, pad -> padding_max
        :param beta: if min(cw, ch) -> beta, pad -> 0
        :return: off_x, off_y, scale
        """
        scale = max(0, min(cw / w, ch / h))
        return cw / 2 - w * scale / 2, ch / 2 - h * scale / 2, scale

    def _recalc_im(self):
        if self._pixmap is None:
            return

        self._off_x, self._off_y, self._scale = self._calc_smart_centre(
            self._pixmap.width(),
            self._pixmap.height(),
            self.width(),
            self.height()
        )

    def screen_to_im(self, x, y):
        if self._pixmap is None:
            raise ValueError
        return (x - self._off_x) / self._scale, (y - self._off_y) / self._scale

    def im_to_screen(self, x, y):
        return x * self._scale + self._off_x, y * self._scale + self._off_y

    def get_rect(self):
        return QtCore.QRect(
            self._rect_x1,
            self._rect_y1,
            self._rect_x2 - self._rect_x1,
            self._rect_y2 - self._rect_y1
        )

    def get_im_rect(self) -> Tuple[int, int, int, int]:
        x1, y1 = self.screen_to_im(self._rect_x1, self._rect_y1)
        x2, y2 = self.screen_to_im(self._rect_x2, self._rect_y2)

        return (
            x1,
            y1,
            x2,
            y2
        )

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # render background
        brush = QtGui.QBrush(Qt.black, Qt.Dense4Pattern)
        painter.fillRect(0, 0, self.width(), self.height(), brush)

        # render pixmap
        if self._pixmap is not None:
            painter.drawPixmap(
                self._off_x,
                self._off_y,
                self._pixmap.width() * self._scale,
                self._pixmap.height() * self._scale,
                self._pixmap
            )

        # render regions
        if self._regions is not None:
            pen = QtGui.QPen(Qt.red)
            pen.setWidth(2)
            painter.setPen(pen)

            for region in self._regions:
                points = []
                for vertex in region.polygon:
                    points.append(QtCore.QPointF(*self.im_to_screen(*vertex)))
                painter.drawConvexPolygon(QtGui.QPolygonF(points))

        # render rect
        if self.mouse_down:
            if self.draw_rect_border:
                brush = QtGui.QBrush(Qt.blue, Qt.Dense4Pattern)
                pen = QtGui.QPen(Qt.blue)
                pen.setWidth(3)
                pen.setJoinStyle(Qt.MiterJoin)
                pen.setBrush(brush)
                painter.setPen(pen)
                painter.drawRect(self.get_rect())

        # render cursor
        if self._draw_cur:
            cross_radius = 10
            cross_width = 3
            pen = QtGui.QPen(Qt.black)
            pen.setWidth(cross_width)
            painter.setPen(pen)
            painter.drawLine(self.cur_x, self.cur_y - cross_radius, self.cur_x, self.cur_y + cross_radius)
            painter.drawLine(self.cur_x - cross_radius, self.cur_y, self.cur_x + cross_radius, self.cur_y)

            pen.setColor(Qt.white)
            pen.setWidth(cross_width - 2)
            painter.setPen(pen)
            painter.drawLine(self.cur_x, self.cur_y - cross_radius, self.cur_x, self.cur_y + cross_radius)
            painter.drawLine(self.cur_x - cross_radius, self.cur_y, self.cur_x + cross_radius, self.cur_y)

    def resizeEvent(self, event):
        self._recalc_im()
        super().resizeEvent(event)

    def _clamp_x(self, x):
        if self._pixmap is None:
            return x
        return max(self._off_x, min(self._off_x + self._pixmap.width() * self._scale, x))

    def _clamp_y(self, y):
        if self._pixmap is None:
            return y
        return max(self._off_y, min(self._off_y + self._pixmap.height() * self._scale, y))

    def mousePressEvent(self, event):
        self.mouse_down = True
        self._rect_x1 = self._clamp_x(self.cur_x)
        self._rect_y1 = self._clamp_y(self.cur_y)

        if self.callback_mouse_press is not None:
            self.callback_mouse_press(event)

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        self.cur_x, self.cur_y = x, y

        self._rect_x2 = self._clamp_x(self.cur_x)
        self._rect_y2 = self._clamp_y(self.cur_y)
        self.repaint()

        if self.callback_mouse_move is not None:
            self.callback_mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.mouse_down = False
        self.repaint()

        if self.callback_mouse_release is not None:
            self.callback_mouse_release(event)

    def enterEvent(self, event):
        self.setCursor(Qt.BlankCursor)
        self._draw_cur = True

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self._draw_cur = False
        self.repaint()

    def set_regions(self, regions):
        self._regions = tuple(regions)
        self.repaint()