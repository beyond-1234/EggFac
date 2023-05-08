from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import (InfoBar, InfoBarPosition)

class NotifyUtil(QWidget):

    @staticmethod
    def successNotify(parent, title, content):
        InfoBar.success(
                title=title,
                content=content,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
        )
