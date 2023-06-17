# coding:utf-8
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QFont, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QPushButton, QTreeWidgetItem, QTreeWidgetItemIterator, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidgetItem

from qfluentwidgets import ComboBox, LineEdit, PixmapLabel, ScrollArea, ToolButton, ToolTipFilter, TreeWidget, isDarkTheme, FluentIcon, FluentIcon, ListWidget
from ..common.style_sheet import StyleSheet
from ..common.entity.task import Task

class TaskInitWidget(QWidget):
    """ task list """

    def __init__(self, parent: QWidget | None, task: Task) -> None:
        super().__init__(parent)
        # header part
        self.vBoxLayout = QVBoxLayout(self)

        title = QLabel("Output Settings", self)
        title.setObjectName("titleLabel")
        formatLayout = QHBoxLayout(self)
        self.formatLabel = QLabel("Output Format", self)
        trackLabel = QLabel("Track info", self)
        trackList = ListWidget(self)

        self.formatCombo = ComboBox(self)
        self.formatCombo.addItems(['MP4', 'MKV', 'FLV'])
        self.formatCombo.setCurrentIndex(0)

        tracks = task.tracks
        for t in tracks:
            trackItem = QListWidgetItem("{} track: {}".format(t.type, t.name))
            trackList.addItem(trackItem)

        formatLayout.addWidget(self.formatLabel)
        formatLayout.addWidget(self.formatCombo)

        self.vBoxLayout.addWidget(title)
        self.vBoxLayout.addLayout(formatLayout)
        self.vBoxLayout.addWidget(trackLabel)
        self.vBoxLayout.addWidget(trackList)



