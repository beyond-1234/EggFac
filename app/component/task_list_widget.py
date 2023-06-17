# coding:utf-8
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QFont, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from qfluentwidgets import LineEdit, PixmapLabel, ScrollArea, ToolButton, ToolTipFilter, isDarkTheme, FluentIcon, FluentIcon, ProgressBar
from ..common.style_sheet import StyleSheet
from ..common.entity.task import Task
from ..common.signal_bus import signalBus

class TaskListItemWidget(QFrame):
    """ list item """
    def __init__(self, parent: QWidget, task: Task):
        super().__init__(parent)
        self.task = task
        self.outerLayout = QVBoxLayout(self)
        self.infoLayout = QHBoxLayout(self)
        self.buttonLayout = QVBoxLayout(self)
        self.parentLayout = parent

        self.setStyleSheet("TaskListItemWidget{margin-left:8px;margin-right:8px;border: 1px solid grey;border-radius:8px;}")
        self.infoLayout.setContentsMargins(4, 4, 4, 36)
        self.buttonLayout.setContentsMargins(4, 0, 4, 8)

        fileNameLabel = QLabel(task.name, self)
        fileNameLabel.setFont(QFont('Microsoft YaHei', 12, 64, False))

        self.hintLabel = QLabel("progressing", self)
        self.hintLabel.setFont(QFont('Microsoft YaHei', 10, 32, False))

        self.progress = ProgressBar(self)
        self.progress.setValue(0)

        startButton = ToolButton(FluentIcon.CARE_RIGHT_SOLID)
        startButton.clicked.connect(self.startTask)
        startButton.setIconSize(QSize(12, 12))

        deleteButton = ToolButton(FluentIcon.DELETE)
        deleteButton.clicked.connect(self.deleteTaskItem)
        deleteButton.setIconSize(QSize(12, 12))

        self.infoLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.infoLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.buttonLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.infoLayout.addWidget(fileNameLabel, 1, alignment=Qt.AlignLeft)
        self.infoLayout.addWidget(startButton, 0, alignment=Qt.AlignRight)
        self.infoLayout.addWidget(deleteButton, 0, alignment=Qt.AlignRight)

        self.buttonLayout.addWidget(self.progress)
        self.buttonLayout.addWidget(self.hintLabel, 0, Qt.AlignRight)

        self.outerLayout.addLayout(self.infoLayout)
        self.outerLayout.addLayout(self.buttonLayout)


    def deleteTaskItem(self):
        print('delete item')
        self.parentLayout.vBoxLayout.removeWidget(self)

        self.task.deleteTask()

    def updateProgressView(self, code, percentage):
        if self.task.code == code:
            # print("uuid {} ui progress update {}".format(code, percentage))
            self.progress.setValue(percentage)
            if percentage >= 100:
                self.hintLabel.setText("finished")

    def startTask(self):
        print('start item')
        self.hintLabel.setText("progressing")
        signalBus.updateProgressSignal.connect(self.updateProgressView)
        self.task.startTask()



class TaskListWidget(QWidget):
    """ task list """

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # header part
        self.vBoxLayout = QVBoxLayout(self)

    def addTaskItem(self, task):
        print('add item')
        item = TaskListItemWidget(self, task)
        self.vBoxLayout.addWidget(item)
