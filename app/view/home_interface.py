# coding:utf-8
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from qfluentwidgets import LineEdit, PixmapLabel, ScrollArea, ToolButton, ToolTipFilter, isDarkTheme, FluentIcon, FluentIcon
from ..common.style_sheet import StyleSheet


class HeaderWidget(QWidget):
    """ header """

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        # header part
        self.hBoxLayout = QHBoxLayout(self)
        imageScale = 64

        # add task button
        # self.addButton = ToolButton(':/gallery/images/kunkun.png')
        self.addButton = ToolButton(FluentIcon.ADD)
        self.addButton.setIconSize(QSize(imageScale, imageScale))

        self.hBoxLayout.setContentsMargins(16, 16, 16, 16)
        self.hBoxLayout.setSpacing(32)
        self.hBoxLayout.setAlignment(Qt.AlignRight)
        self.hBoxLayout.addWidget(self.addButton, 0, Qt.AlignRight)



class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        # overall vertical layout
        self.vBoxLayoutForAll = QVBoxLayout(self.view)
        # header part
        self.headerWidget = HeaderWidget(self)

        self.__initWidget()
        # self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayoutForAll.addWidget(self.headerWidget)
        self.vBoxLayoutForAll.setAlignment(Qt.AlignTop)

    # def loadSamples(self):
    #     """ load samples """
    #     pass
