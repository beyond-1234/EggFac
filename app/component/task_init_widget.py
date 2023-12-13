# coding:utf-8
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import (
    QDesktopServices,
    QFont,
    QPixmap,
    QPainter,
    QColor,
    QBrush,
    QPainterPath,
)
from PyQt5.QtWidgets import (
    QFrame,
    QPushButton,
    QTreeWidgetItem,
    QTreeWidgetItemIterator,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidgetItem,
)

from qfluentwidgets import ComboBox, CheckBox

from ..common.entity.task import Task
from .track_info_widget import TrackInfoWidget
from ..common.signal_bus import signalBus


class TaskInitWidget(QWidget):
    """task list"""

    def __init__(self, parent: QWidget | None, task: Task) -> None:
        super().__init__(parent)
        # header part
        self.vBoxLayout = QVBoxLayout(self)
        self.taskInstace = task

        title = QLabel("Output Settings", self)
        title.setObjectName("titleLabel")

        formatLayout = QHBoxLayout(self)
        self.formatLabel = QLabel("Output Format", self)
        self.formatCombo = ComboBox(self)
        self.formatCombo.addItems(["MP4", "MKV", "FLV"])
        self.formatCombo.setCurrentIndex(0)
        formatLayout.addWidget(self.formatLabel)
        formatLayout.addWidget(self.formatCombo)

        keepSettingLayout = QHBoxLayout(self)
        keepSettingLabel = QLabel(self.tr("keep original setting"), self)
        isKeepingSettingCheckBox = CheckBox("", self)
        isKeepingSettingCheckBox.setChecked(True)
        isKeepingSettingCheckBox.stateChanged.connect(slot=self.onKeepOriginalChanged)

        keepSettingLayout.addWidget(keepSettingLabel)
        keepSettingLayout.addWidget(isKeepingSettingCheckBox)

        # self.t = TrackInfoWidget(self, task)

        self.vBoxLayout.addWidget(title)
        self.vBoxLayout.addLayout(formatLayout)
        self.vBoxLayout.addLayout(keepSettingLayout)
        # self.vBoxLayout.addWidget(self.t)

        signalBus.dialogYesButtonSignal.connect(self.yesButtonClickEvent)

    def yesButtonClickEvent(self):
        f = self.formatCombo.currentText()
        signalBus.updateTaskTargetFormatSignal.emit(self.taskInstace.code, f)

    def onKeepOriginalChanged(self, state):
        if state == 0:
            signalBus.updateTaskIsKeepOriginalSignal.emit(self.taskInstace.code, False)
        elif state == 2:
            signalBus.updateTaskIsKeepOriginalSignal.emit(self.taskInstace.code, True)
