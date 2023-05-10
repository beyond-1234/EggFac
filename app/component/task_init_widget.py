# coding:utf-8
import typing
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl, Qt, QRectF
from PyQt5.QtGui import QDesktopServices, QFont, QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QFrame, QPushButton, QTreeWidgetItem, QTreeWidgetItemIterator, QWidget, QHBoxLayout, QVBoxLayout, QLabel

from qfluentwidgets import ComboBox, LineEdit, PixmapLabel, ScrollArea, ToolButton, ToolTipFilter, TreeWidget, isDarkTheme, FluentIcon, FluentIcon
from ..common.style_sheet import StyleSheet

class TaskInitWidget(QWidget):
    """ task list """

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        # header part
        self.vBoxLayout = QVBoxLayout(self)

        title = QLabel("Output Settings", self)
        title.setObjectName("titleLabel")

        formatLayout = QHBoxLayout(self)

        formatLabel = QLabel("Output Format", self)

        formatCombo = ComboBox(self)
        formatCombo.addItems(['MP4', 'MKV', 'FLV'])
        formatCombo.setCurrentIndex(0)

        trackLabel = QLabel("Track info", self)

        tree = TreeWidget(self)
        videoItem = QTreeWidgetItem(['Video tracks'])
        videoItem.addChildren([
            QTreeWidgetItem(['video track 1'])
            ])
        audioItem = QTreeWidgetItem(['Audio tracks'])
        audioItem.addChildren([
            QTreeWidgetItem(['audio track 1'])
            ])
        subtitleItem = QTreeWidgetItem(['Subtitle tracks'])
        subtitleItem.addChildren([
            QTreeWidgetItem(['subtitle track 1'])
            ])

        tree.addTopLevelItems([videoItem, audioItem, subtitleItem])

        tree.expandAll()
        tree.setHeaderHidden(True)

        formatLayout.addWidget(formatLabel)
        formatLayout.addWidget(formatCombo)

        self.vBoxLayout.addWidget(title)
        self.vBoxLayout.addLayout(formatLayout)
        self.vBoxLayout.addWidget(trackLabel)
        self.vBoxLayout.addWidget(tree)



