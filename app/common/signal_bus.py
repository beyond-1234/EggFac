# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """Signal bus"""

    switchToSampleCard = pyqtSignal(str, int)
    updateProgressSignal = pyqtSignal(str, int)
    dialogYesButtonSignal = pyqtSignal()
    changeDetailDisplaySignal = pyqtSignal(str, int)
    generateFFmpegCommandSignal = pyqtSignal(str)
    updateTaskPidSignal = pyqtSignal(str, int)
    updateTaskTargetFormatSignal = pyqtSignal(str, str)
    updateTaskIsKeepOriginalSignal = pyqtSignal(str, bool)
    updateTaskCommandSignal = pyqtSignal(str)
    startTaskSignal = pyqtSignal(str)
    deleteTaskSignal = pyqtSignal(str)


signalBus = SignalBus()
