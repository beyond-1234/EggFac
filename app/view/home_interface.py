# coding:utf-8
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QFont, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QProgressBar, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog
from qfluentwidgets import (InfoBar, InfoBarPosition, PixmapLabel,
                            PushButton, ScrollArea, ToolButton, StrongBodyLabel,
                            ToolTipFilter, isDarkTheme, FluentIcon, FluentIcon, Action, CommandBar)
from app.component.dialog import CustomDialog
from app.component.task_init_widget import TaskInitWidget
from app.component.task_list_widget import TaskListWidget
from app.component.task_detail_widget import TaskDetailWidget
from ..common.entity.task import Task
from ..common.style_sheet import StyleSheet


class HeaderWidget(QWidget):
    """ header """

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        # header part
        self.hBoxLayout = QHBoxLayout(self)

        self.addAction = Action(FluentIcon.ADD, self.tr("Add"))

        bar = CommandBar()
        # need to set width if having multiple buttons
        # otherwise buttons will collapse
        bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        bar.addActions([
            self.addAction
        ])

        #  self.addLabel = QLabel("Add new task", self)
        #  self.addLabel.setFont(QFont('Microsoft YaHei', 32, 0, False))
#
        self.taskLabel = StrongBodyLabel("Task list", self)
#
        #  add task button
        #  self.addButton = ToolButton(FluentIcon.ADD)
        #  self.addButton.setIconSize(QSize(imageScale, imageScale))
#
        self.hBoxLayout.setContentsMargins(18, 18, 18, 0)
        #  self.hBoxLayout.setSpacing(32)
        #  self.hBoxLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        self.hBoxLayout.addWidget(self.taskLabel, 1, Qt.AlignLeft)
        #  self.hBoxLayout.addWidget(self.addLabel, 0, Qt.AlignRight)
        #  self.hBoxLayout.addWidget(self.addButton, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(bar, 0, Qt.AlignRight)


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        # overall vertical layout
        self.vBoxLayoutForAll = QVBoxLayout(self.view)
        # header part
        self.headerWidget = HeaderWidget(self)
        self.headerWidget.addAction.triggered.connect(self.clickAddButton)

        self.lineSpliter = QFrame(self)
        self.lineSpliter.setObjectName("lineSpliter")
        self.lineSpliter.setStyleSheet("QFrame#lineSpliter{color:lightgrey;height:1px;margin-left:18px;margin-right:32px;}")
        self.lineSpliter.setFrameShape(QFrame.Shape.HLine)

        # task list
        self.taskList = TaskListWidget(self)

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName('view')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.vBoxLayoutForAll.setAlignment(Qt.AlignTop)

        self.vBoxLayoutForAll.addWidget(self.headerWidget)
        self.vBoxLayoutForAll.addWidget(self.lineSpliter)
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

        task = Task.initTaskOnlySource(file[0])

        if task is None:
            return

        # open init task dialog
        taskInitDialog = CustomDialog(TaskInitWidget(self, task), task, self)
        if not taskInitDialog.exec():
            print('cancel clicked')
            return

        if not task.isKeepingOriginalSeting:
            # open detail setting dialog
            taskDetailDialog = CustomDialog(TaskDetailWidget(self, task), task, self, 600)
            if not taskDetailDialog.exec():
                print('cancel detail clicked')
                return

        self.taskList.addTaskItem(task)


    def checkFile(self, filePath):
        return True
