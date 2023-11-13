from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem, QFrame
from qfluentwidgets import CheckBox, SpinBox, LineEdit, Pivot, qrouter, ListWidget, FlowLayout, StrongBodyLabel

from ..entity.task import Task
from ..entity.track import Track

class PropCheckEdit(QWidget):
    """ property check edit """

    def __init__(self, parent, label, valueChanged):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)

        checkBox = CheckBox(label)
        checkBox.stateChanged.connect(valueChanged)

        self.hBoxLayout.addWidget(checkBox, 1)

