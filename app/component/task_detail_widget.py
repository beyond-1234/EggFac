from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem, QFrame
from qfluentwidgets import SpinBox, LineEdit, Pivot, SpinBox, qrouter, ListWidget, FlowLayout, StrongBodyLabel

from ..common.entity.task import Task
from ..common.entity.track import Track
from ..common.prop_line_edit import PropLineEdit

class TaskDetailWidget(QWidget):
    """ track info pivot page """

    def __init__(self, parent, task: Task):
        super().__init__(parent=parent)

        self.stackedWidget = QStackedWidget(self)
        self.pivot = Pivot(self)
        self.vBoxLayout = QVBoxLayout(self)

        # self.videoTrackInterface = VideoSubPage(self, task)
        # self.audioTrackInterface = AudioSubPage(self, task)
        # self.subtitleTrackInterface = SubtitleSubPage(self, task)

        # self.addSubPivotPage(self.videoTrackInterface, 'Video', self.tr('Video'))
        # self.addSubPivotPage(self.subtitleTrackInterface, 'Subtitle', self.tr('Subtitle'))

        videoPage = self.addVideoPage(task)
        self.addAudioPage(task)
        self.addSubtitlePage(task)

        self.vBoxLayout.addWidget(self.pivot, 0)
        self.vBoxLayout.addWidget(self.stackedWidget, 0)
        self.vBoxLayout.setContentsMargins(0,0,0,0)

        self.stackedWidget.currentChanged.connect(slot=self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(videoPage)
        self.pivot.setCurrentItem(videoPage.objectName())


    def addVideoPage(self, task):
        subPage = TrackSubPage(self, task, 'video')

        sampleRateEdit = PropLineEdit(
                self,
                self.tr('Sample Rate'),
                task.taskDetail.audioSampleRate,
                lambda t: task.taskDetail.setAudioSampleRate(t),
                minn=1,
                maxn=2147483647,
                unit='Hz')

        bitRateEdit = PropLineEdit(
                self,
                self.tr('Bit Rate'),
                task.taskDetail.audioBitRate,
                lambda t: task.taskDetail.setAudioBitRate(t),
                minn=1,
                maxn=2147483647,
                unit='kb/s')

        volumnEdit = PropLineEdit(
                self,
                self.tr('Volumn'),
                task.taskDetail.audioVolumn,
                lambda t: task.taskDetail.setAudioVolumn(t),
                minn=1,
                maxn=100,
                unit='%')

        subPage.addPropWidget(sampleRateEdit)
        subPage.addPropWidget(bitRateEdit)
        subPage.addPropWidget(volumnEdit)
        self.addSubPivotPage(subPage, 'Video', self.tr('Video'))
        return subPage


    def addAudioPage(self, task):
        subPage = TrackSubPage(self, task, 'audio')

        sampleRateEdit = PropLineEdit(
                self,
                self.tr('Sample Rate'),
                task.taskDetail.audioSampleRate,
                lambda t: task.taskDetail.setAudioSampleRate(t),
                minn=1,
                maxn=2147483647,
                unit='Hz')

        bitRateEdit = PropLineEdit(
                self,
                self.tr('Bit Rate'),
                task.taskDetail.audioBitRate,
                lambda t: task.taskDetail.setAudioBitRate(t),
                minn=1,
                maxn=2147483647,
                unit='kb/s')

        volumnEdit = PropLineEdit(
                self,
                self.tr('Volumn'),
                task.taskDetail.audioVolumn,
                lambda t: task.taskDetail.setAudioVolumn(t),
                minn=1,
                maxn=100,
                unit='%')

        subPage.addPropWidget(sampleRateEdit)
        subPage.addPropWidget(bitRateEdit)
        subPage.addPropWidget(volumnEdit)
        self.addSubPivotPage(subPage, 'Audio', self.tr('Audio'))

    def addSubtitlePage(self, task):
        subPage = TrackSubPage(self, task, 'subtitle')

        sampleRateEdit = PropLineEdit(
                self,
                self.tr('Sample Rate'),
                task.taskDetail.audioSampleRate,
                lambda t: task.taskDetail.setAudioSampleRate(t),
                minn=1,
                maxn=2147483647,
                unit='Hz')

        bitRateEdit = PropLineEdit(
                self,
                self.tr('Bit Rate'),
                task.taskDetail.audioBitRate,
                lambda t: task.taskDetail.setAudioBitRate(t),
                minn=1,
                maxn=2147483647,
                unit='kb/s')

        volumnEdit = PropLineEdit(
                self,
                self.tr('Volumn'),
                task.taskDetail.audioVolumn,
                lambda t: task.taskDetail.setAudioVolumn(t),
                minn=1,
                maxn=100,
                unit='%')

        subPage.addPropWidget(sampleRateEdit)
        subPage.addPropWidget(bitRateEdit)
        subPage.addPropWidget(volumnEdit)
        self.addSubPivotPage(subPage, 'Subtitle', self.tr('Subtitle'))


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

class TrackSubPage(QWidget):

    def __init__(self, parent: QWidget | None, task: Task, page: str) -> None:
        super().__init__(parent)
        # header part
        audioDetailLayout = QHBoxLayout(self)

        trackList = ListWidget(self)

        virtualParent = QWidget()
        self.layout = FlowLayout(virtualParent, False)

        lineSpliter = QFrame(self)
        lineSpliter.setObjectName("lineSpliterDetail")
        lineSpliter.setStyleSheet("QFrame#lineSpliterDetail{color:lightgrey;widget:4px;height:100%;}")
        lineSpliter.setFrameShape(QFrame.Shape.VLine)

        tracks = task.tracks
        for t in tracks:
            if t.type == page:
                trackItem = QListWidgetItem(t.name)
                trackItem.setCheckState(Qt.Checked)
                trackList.addItem(trackItem)

        audioDetailLayout.addWidget(trackList)
        audioDetailLayout.addWidget(lineSpliter)
        audioDetailLayout.addWidget(virtualParent)

        audioDetailLayout.setStretch(0, 1)
        audioDetailLayout.setStretch(1, 1)
        audioDetailLayout.setStretch(2, 4)

    def addPropWidget(self, widget):
        self.layout.addWidget(widget)
