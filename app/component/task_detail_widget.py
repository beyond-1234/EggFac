from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem, QFrame
from qfluentwidgets import Pivot, qrouter, ListWidget

from ..common.entity.task import Task
from ..common.entity.track import Track

class TaskDetailWidget(QWidget):
    """ track info pivot page """

    def __init__(self, parent, task: Task):
        super().__init__(parent=parent)

        self.stackedWidget = QStackedWidget(self)
        self.pivot = Pivot(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.videoTrackInterface = VideoSubPage(self, task)
        self.audioTrackInterface = AudioSubPage(self, task)
        self.subtitleTrackInterface = SubtitleSubPage(self, task)

        self.addSubPivotPage(self.videoTrackInterface, 'Video', self.tr('Video'))
        self.addSubPivotPage(self.audioTrackInterface, 'Audio', self.tr('Audio'))
        self.addSubPivotPage(self.subtitleTrackInterface, 'Subtitle', self.tr('Subtitle'))

        self.vBoxLayout.addWidget(self.pivot, 0)
        self.vBoxLayout.addWidget(self.stackedWidget, 0)
        self.vBoxLayout.setContentsMargins(0,0,0,0)

        self.stackedWidget.currentChanged.connect(slot=self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.videoTrackInterface)
        self.pivot.setCurrentItem(self.videoTrackInterface.objectName())

    def addSubPivotPage(self, widget, routeKey, title):
        # widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        widget.setObjectName(routeKey)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
                routeKey=routeKey,
                text=title,
                onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

class VideoSubPage(QWidget):

    def __init__(self, parent: QWidget | None, task: Task) -> None:
        super().__init__(parent)
        # header part
        self.vBoxLayout = QHBoxLayout(self)

        trackList = ListWidget(self)
        trackList.setDisabled(True)

        tracks = task.tracks
        for t in tracks:
            if t.type == 'video':
                trackItem = QListWidgetItem("{}".format(t.type, t.name))
                trackList.addItem(trackItem)

        #  trackList.setCurrentRow(0)
        self.vBoxLayout.addWidget(trackList)

class AudioSubPage(QWidget):

    def __init__(self, parent: QWidget | None, task: Task) -> None:
        super().__init__(parent)
        # header part
        self.vBoxLayout = QVBoxLayout(self)

        trackList = ListWidget(self)
        trackList.setDisabled(True)
        #  trackList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        #  trackList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        tracks = task.tracks
        for t in tracks:
            if t.type == 'audio':
                trackItem = QListWidgetItem("{} track: {}".format(t.type, t.name))
                trackList.addItem(trackItem)

        #  trackList.setCurrentRow(0)
        self.vBoxLayout.addWidget(trackList)

class SubtitleSubPage(QWidget):

    def __init__(self, parent: QWidget | None, task: Task) -> None:
        super().__init__(parent)
        # header part
        self.vBoxLayout = QVBoxLayout(self)

        trackList = ListWidget(self)
        trackList.setDisabled(True)
        #  trackList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        #  trackList.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        tracks = task.tracks
        for t in tracks:
            if t.type == 'subtitle':
                trackItem = QListWidgetItem("{} track: {}".format(t.type, t.name))
                trackList.addItem(trackItem)

        self.vBoxLayout.addWidget(trackList)

