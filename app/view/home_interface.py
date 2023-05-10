# coding:utf-8
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QFont, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QProgressBar, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog
from qfluentwidgets import (InfoBar, InfoBarPosition, PixmapLabel,
                            PushButton, ScrollArea, ToolButton,
                            ToolTipFilter, isDarkTheme, FluentIcon, FluentIcon)
from app.component.dialog import CustomDialog
from app.component.task_init_widget import TaskInitWidget
from app.component.task_list_widget import TaskListWdget
from ..common.style_sheet import StyleSheet


class HeaderWidget(QWidget):
    """ header """

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        # header part
        self.hBoxLayout = QHBoxLayout(self)
        imageScale = 64

        self.addLabel = QLabel("Add new task", self)
        self.addLabel.setFont(QFont('Microsoft YaHei', 32, 0, False))

        # add task button
        self.addButton = ToolButton(FluentIcon.ADD)
        self.addButton.setIconSize(QSize(imageScale, imageScale))

        self.hBoxLayout.setContentsMargins(16, 16, 16, 16)
        self.hBoxLayout.setSpacing(32)
        self.hBoxLayout.setAlignment(Qt.AlignRight)
        self.hBoxLayout.addWidget(self.addLabel, 0, Qt.AlignRight)
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
        self.headerWidget.addButton.clicked.connect(self.clickAddButton)

        # task list
        self.taskList = TaskListWdget(self)

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.vBoxLayoutForAll.setAlignment(Qt.AlignTop)

        self.vBoxLayoutForAll.addWidget(self.headerWidget)
        self.vBoxLayoutForAll.addWidget(self.taskList)

    def clickAddButton(self):
        print('click add button')
        file = QFileDialog.getOpenFileName(
            self,
            self.tr("Choose file"),
            "./")
        print(file[0])

        if not self.checkFile(filePath=file[0]):
            return

        dia = CustomDialog(TaskInitWidget(self), self)
        if dia.exec():
            print('ok clicked')
        else:
            print('cancel clicked')
        self.taskList.addTaskItem()

    def checkFile(self, filePath):
        return True
