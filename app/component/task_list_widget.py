# coding:utf-8
import subprocess
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QFrame,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
)

from qfluentwidgets import (
    ToolButton,
    FluentIcon,
    ProgressBar,
)
from ..common.entity.task import Task
from ..common.entity.task_status import TaskStatus
from ..common.signal_bus import signalBus
from ..common.config import cfg


class TaskListItemWidget(QFrame):
    """list item"""

    def __init__(self, parent: QWidget, task: Task):
        super().__init__(parent)
        self.task = task
        self.outerLayout = QVBoxLayout(self)
        self.infoLayout = QHBoxLayout(self)
        self.buttonLayout = QVBoxLayout(self)
        self.parentLayout = parent

        self.setStyleSheet(
            "TaskListItemWidget{margin-left:8px;margin-right:8px;border: 1px solid grey;border-radius:8px;}"
        )
        self.infoLayout.setContentsMargins(4, 4, 4, 36)
        self.buttonLayout.setContentsMargins(4, 0, 4, 8)

        fileNameLabel = QLabel(task.name, self)
        fileNameLabel.setFont(QFont("Microsoft YaHei", 12, 64, False))
        fileNameLabel.setMaximumWidth(600)

        self.hintLabel = QLabel("", self)
        self.hintLabel.setFont(QFont("Microsoft YaHei", 10, 32, False))

        self.progress = ProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.startButton = ToolButton(FluentIcon.CARE_RIGHT_SOLID)
        self.startButton.clicked.connect(self.startTask)
        self.startButton.setIconSize(QSize(12, 12))

        deleteButton = ToolButton(FluentIcon.DELETE)
        deleteButton.clicked.connect(self.deleteTaskItem)
        deleteButton.setIconSize(QSize(12, 12))

        openButton = ToolButton(FluentIcon.FOLDER)
        openButton.clicked.connect(self.openTargetFolder)
        openButton.setIconSize(QSize(12, 12))

        self.infoLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.infoLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.buttonLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.infoLayout.addWidget(fileNameLabel, 1, alignment=Qt.AlignLeft)
        self.infoLayout.addWidget(self.startButton, 0, alignment=Qt.AlignRight)
        self.infoLayout.addWidget(deleteButton, 0, alignment=Qt.AlignRight)
        self.infoLayout.addWidget(openButton, 0, alignment=Qt.AlignRight)

        self.buttonLayout.addWidget(self.progress)
        self.buttonLayout.addWidget(self.hintLabel, 0, Qt.AlignRight)

        self.outerLayout.addLayout(self.infoLayout)
        self.outerLayout.addLayout(self.buttonLayout)

        signalBus.updateViewTaskStatusSignal.connect(self.updateTaskStatus)

    def deleteTaskItem(self):
        self.parentLayout.vBoxLayout.removeWidget(self)

        signalBus.deleteTaskSignal.emit(self.task.code)

    def openTargetFolder(self):
        subprocess.Popen(["xdg-open", cfg.outputFolder.value])

    def updateProgressView(self, code, percentage):
        if self.task.code == code:
            self.progress.setValue(percentage)
            if percentage >= 100:
                self.hintLabel.setText(self.tr("Done"))
            else:
                self.hintLabel.setText(f"{percentage}%")

    def startTask(self):
        if self.task.status == TaskStatus.CREATED:
            signalBus.startTaskSignal.emit(self.task.code)
        elif self.task.status == TaskStatus.STARTED:
            signalBus.stopTaskSignal.emit(self.task.code)
        elif self.task.status == TaskStatus.ENDED:
            signalBus.startTaskSignal.emit(self.task.code)

        signalBus.updateProgressSignal.connect(self.updateProgressView)

    def updateTaskStatus(self, taskCode, taskStatus):
        if self.task.code == taskCode:
            if taskStatus == TaskStatus.CREATED:
                self.startButton.setIcon(FluentIcon.CARE_RIGHT_SOLID)
            elif taskStatus == TaskStatus.STARTED:
                self.startButton.setIcon(FluentIcon.PAUSE)
            elif taskStatus == TaskStatus.ENDED:
                self.startButton.setIcon(FluentIcon.CARE_RIGHT_SOLID)


class TaskListWidget(QWidget):
    """task list"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # header part
        self.vBoxLayout = QVBoxLayout(self)

    def addTaskItem(self, task):
        item = TaskListItemWidget(self, task)
        self.vBoxLayout.addWidget(item)
