# coding:utf-8
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QFont, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QProgressBar, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from qfluentwidgets import LineEdit, PixmapLabel, ScrollArea, ToolButton, ToolTipFilter, isDarkTheme, FluentIcon, FluentIcon
from ..common.style_sheet import StyleSheet
from ..common.entity.task import Task

class TaskListItemWdget(QWidget):
    """ list item """
    def __init__(self, parent: QWidget, task: Task):
        super().__init__(parent)
        self.task = task
        self.outerLayout = QHBoxLayout(self)
        self.infoLayout = QHBoxLayout(self)
        self.buttonLayout = QHBoxLayout(self)
        self.parentLayout = parent

        fileNameLabel = QLabel(task.name, self)
        fileNameLabel.setFont(QFont('Microsoft YaHei', 14, 0, False))
        fileNameLabel.setFixedWidth(150)

        progress = QProgressBar(self)
        progress.setValue(20)
        progress.setMaximum(100)
        progress.setMinimum(0)

        startButton = ToolButton(FluentIcon.CARE_RIGHT_SOLID)
        startButton.clicked.connect(self.startTask)

        deleteButton = ToolButton(FluentIcon.DELETE)
        deleteButton.clicked.connect(self.deleteTaskItem)

        self.infoLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.infoLayout.setSpacing(4)
        self.buttonLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.buttonLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.infoLayout.addWidget(fileNameLabel, 0, alignment=Qt.AlignLeft)
        self.infoLayout.addWidget(progress)

        self.buttonLayout.addWidget(startButton, 0, alignment=Qt.AlignRight)
        self.buttonLayout.addWidget(deleteButton, 0, alignment=Qt.AlignRight)

        self.outerLayout.addLayout(self.infoLayout)
        self.outerLayout.addLayout(self.buttonLayout)


    def deleteTaskItem(self):
        print('delete item')
        self.parentLayout.vBoxLayout.removeWidget(self)

        self.task.deleteTask()

    def startTask(self):
        print('start item')
        self.task.startTask()



class TaskListWdget(QWidget):
    """ task list """

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        # header part
        self.vBoxLayout = QVBoxLayout(self)

        addLabel = QLabel("Task list", self)
        addLabel.setFont(QFont('Microsoft YaHei', 32, 0, False))

        self.vBoxLayout.addWidget(addLabel)

    def addTaskItem(self, task):
        print('add item')
        item = TaskListItemWdget(self, task)
        self.vBoxLayout.addWidget(item)
