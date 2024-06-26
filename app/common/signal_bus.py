# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal

from app.common.entity.task_status import TaskStatus


class SignalBus(QObject):
    """Signal bus"""

    switchToSampleCard = pyqtSignal(str, int)
    updateProgressSignal = pyqtSignal(str, int)
    updateViewTaskStatusSignal = pyqtSignal(str, TaskStatus)
    dialogYesButtonSignal = pyqtSignal()
    changeDetailDisplaySignal = pyqtSignal(str, int)
    generateFFmpegCommandSignal = pyqtSignal(str)
    updateTaskPidSignal = pyqtSignal(str, int)
    updateTaskTargetFormatSignal = pyqtSignal(str, str)
    updateTaskIsKeepOriginalSignal = pyqtSignal(str, bool)
    updateTaskCommandSignal = pyqtSignal(str, dict)
    startTaskSignal = pyqtSignal(str)
    stopTaskSignal = pyqtSignal(str)
    deleteTaskSignal = pyqtSignal(str)


signalBus = SignalBus()
