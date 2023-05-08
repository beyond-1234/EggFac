# coding:utf-8
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QFont, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from qfluentwidgets import LineEdit, PixmapLabel, ScrollArea, ToolButton, ToolTipFilter, isDarkTheme, FluentIcon, FluentIcon
from ..common.style_sheet import StyleSheet

class TaskListItemWdget(QWidget):
    """ list item """
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)

        addLabel = QLabel("Task", self)
        addLabel.setFont(QFont('Microsoft YaHei', 16, 0, False))
        self.parentLayout = parent

        deleteButton = ToolButton(FluentIcon.DELETE)
        deleteButton.clicked.connect(self.deleteTaskItem)

        self.hBoxLayout.addWidget(addLabel)
        self.hBoxLayout.addWidget(deleteButton)

    def deleteTaskItem(self):
        print('delete item')
        self.parentLayout.vBoxLayout.removeWidget(self)



class TaskListWdget(QWidget):
    """ task list """

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        # header part
        self.vBoxLayout = QVBoxLayout(self)

        addLabel = QLabel("Task list", self)
        addLabel.setFont(QFont('Microsoft YaHei', 32, 0, False))

        self.vBoxLayout.addWidget(addLabel)

    def addTaskItem(self):
        print('add item')
        item = TaskListItemWdget(self)
        self.vBoxLayout.addWidget(item)
