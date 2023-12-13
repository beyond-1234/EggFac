# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """Signal bus"""

    switchToSampleCard = pyqtSignal(str, int)
    updateProgressSignal = pyqtSignal(str, int)
    dialogYesButtonSignal = pyqtSignal(str)
    generateFFmpegCommandSignal = pyqtSignal(str)
    updateTaskPidSignal = pyqtSignal(str, int)
    updateTaskTargetFormatSignal = pyqtSignal(str, str)
    updateTaskIsKeepOriginalSignal = pyqtSignal(str, str)


signalBus = SignalBus()
