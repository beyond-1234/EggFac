from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import (
    QSizePolicy,
    QSpacerItem,
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QFrame,
)
from qfluentwidgets import (
    SpinBox,
    LineEdit,
    Pivot,
    SpinBox,
    qrouter,
    ListWidget,
    FlowLayout,
    StrongBodyLabel,
)

from ..common.entity.task import Task
from ..common.entity.track import Track
from ..common.widget.prop_line_edit import PropLineEdit
from ..common.widget.prop_check_edit import PropCheckEdit
from ..common.widget.prop_combo_edit import PropComboEdit
from ..common.signal_bus import signalBus


class TaskDetailWidget(QWidget):
    """track info pivot page"""

    def __init__(self, parent, task: Task):
        super().__init__(parent=parent)

        self.stackedWidget = QStackedWidget(self)
        self.pivot = Pivot(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.task = task

        self.videoPage = self.addVideoPage(task)
        self.addAudioPage(task)
        self.addSubtitlePage(task)

        self.vBoxLayout.addWidget(self.pivot, 0)
        self.vBoxLayout.addWidget(self.stackedWidget, 0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget.currentChanged.connect(slot=self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.videoPage)
        self.pivot.setCurrentItem(self.videoPage.objectName())
        signalBus.changeDetailDisplaySignal.connect(self.updateDetailInfo)

    def updateDetailInfo(self, page: str, index: int):
        if page == "audio":
            self.audioSampleRateEdit.setValue(
                self.task.probe.audioStreams[index].sampling
            )
            self.audioBitRateEdit.setValue(self.task.probe.audioStreams[index].bitrate)
            self.audioVolumnEdit.setValue(100)

    def addVideoPage(self, task: Task):
        subPage = TrackSubPage(self, task, "video", False)

        self.deinterlacingEdit = PropCheckEdit(
            self,
            self.tr("Deinterlacing"),
            lambda t: task.taskDetail.setDeinterlacing(t),
        )

        self.vFlipEdit = PropCheckEdit(
            self, self.tr("Vertical Flip"), lambda t: task.taskDetail.setVerticalFlip(t)
        )

        self.hFlipEdit = PropCheckEdit(
            self,
            self.tr("Horizontal Flip"),
            lambda t: task.taskDetail.setHorizontalFlip(t),
        )

        self.rotateEdit = PropComboEdit(
            self,
            self.tr("Rotation"),
            ["0", "90", "180", "270", "-90", "-180", "-270"],
            lambda t: task.taskDetail.setRotation(t),
        )

        self.bitRateEdit = PropLineEdit(
            self,
            self.tr("Bit Rate"),
            task.probe.bitrate,
            lambda t: task.taskDetail.setVideoBitRate(t),
            minn=1,
            maxn=2147483647,
            unit="kb/s",
        )

        self.speedEdit = PropComboEdit(
            self,
            self.tr("Speed"),
            ["1.0x", "1.25x", "1.5x", "2x", "0.75x", "0.5x"],
            lambda t: task.taskDetail.setSpeed(t),
        )

        self.spacer = QWidget()
        self.spacer.setMinimumWidth(self.width())
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        subPage.addPropWidget(self.deinterlacingEdit)
        subPage.addPropWidget(self.vFlipEdit)
        subPage.addPropWidget(self.hFlipEdit)
        subPage.addPropWidget(self.spacer)
        subPage.addPropWidget(self.rotateEdit)
        subPage.addPropWidget(self.bitRateEdit)
        subPage.addPropWidget(self.speedEdit)
        self.addSubPivotPage(subPage, "Video", self.tr("Video"))
        return subPage

    def addAudioPage(self, task: Task):
        subPage = TrackSubPage(self, task, "audio")

        if len(task.probe.audioStreams) == 0:
            return subPage

        self.audioSampleRateEdit = PropLineEdit(
            self,
            self.tr("Sample Rate"),
            task.probe.audioStreams[0].sampling,
            lambda t: task.taskDetail.setAudioSampleRate(
                subPage.trackList.currentRow(), t
            ),
            minn=1,
            maxn=2147483647,
            unit="Hz",
        )

        self.audioBitRateEdit = PropLineEdit(
            self,
            self.tr("Bit Rate"),
            task.probe.audioStreams[0].bitrate,
            lambda t: task.taskDetail.setAudioBitRate(
                subPage.trackList.currentRow(), t
            ),
            minn=1,
            maxn=2147483647,
            unit="kb/s",
        )

        self.audioVolumnEdit = PropLineEdit(
            self,
            self.tr("Volumn"),
            100,
            lambda t: task.taskDetail.setAudioVolumn(subPage.trackList.currentRow(), t),
            minn=1,
            maxn=200,
            unit="%",
        )

        subPage.addPropWidget(self.audioSampleRateEdit)
        subPage.addPropWidget(self.audioBitRateEdit)
        subPage.addPropWidget(self.audioVolumnEdit)
        self.addSubPivotPage(subPage, "Audio", self.tr("Audio"))

    def addSubtitlePage(self, task):
        subPage = TrackSubPage(self, task, "subtitle")

        self.addSubPivotPage(subPage, "Subtitle", self.tr("Subtitle"))

    def addSubPivotPage(self, widget, routeKey, title):
        # widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        widget.setObjectName(routeKey)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=routeKey,
            text=title,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())


class TrackSubPage(QWidget):
    def __init__(
        self, parent: QWidget | None, task: Task, page: str, isSplite: bool = True
    ) -> None:
        super().__init__(parent)
        self.page = page
        self.detailLayout = QHBoxLayout(self)
        self.virtualParent = QWidget()
        self.propLayout = FlowLayout(self.virtualParent, False)

        # signalBus.generateFFmpegCommandSignal.connect(self.onGeneratingFFmpegCommand)

        if isSplite is True:
            self.trackList = ListWidget(self)
            self.lineSpliter = QFrame(self)

            self.lineSpliter.setObjectName("lineSpliterDetail")
            self.lineSpliter.setStyleSheet(
                "QFrame#lineSpliterDetail{color:lightgrey;width:4px;height:100%;}"
            )
            self.lineSpliter.setFrameShape(QFrame.Shape.VLine)
            tracks = list()
            if page == "video":
                tracks = task.probe.videoStreams
            elif page == "audio":
                tracks = task.probe.audioStreams
            else:
                tracks = task.probe.subtitleStreams

            for t in tracks:
                trackItem = QListWidgetItem(t.codec)
                trackItem.setCheckState(Qt.Checked)
                self.trackList.addItem(trackItem)

            self.trackList.currentItemChanged.connect(self.onTrackChanged)

            self.detailLayout.addWidget(self.trackList)
            self.detailLayout.addWidget(self.lineSpliter)

        self.detailLayout.addWidget(self.virtualParent)
        # if isSplite is True:
        #     self.detailLayout.setStretch(0, 1)
        #     self.detailLayout.setStretch(1, 1)
        #     self.detailLayout.setStretch(2, 4)

    def addPropWidget(self, widget):
        self.propLayout.addWidget(widget)

    def onTrackChanged(self, current):
        """update interface info when changing track"""
        signalBus.changeDetailDisplaySignal.emit(
            self.page, self.trackList.indexFromItem(current).row()
        )

    # def onGeneratingFFmpegCommand(self, code: str):
    #     if self.task.code == code:
    #         self.task.wrapper.fillCommandList(self.task.taskDetail.extraCommand)
