from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem, QFrame
from qfluentwidgets import SpinBox, LineEdit, Pivot, qrouter, ListWidget, FlowLayout, StrongBodyLabel

from ..common.entity.task import Task
from ..common.entity.track import Track

class PropLineEdit(QWidget):
    """ property line edit """

    def __init__(self, parent, label, value, valueChanged,  minn=1, maxn=100, unit=''):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)
        labelWidget = StrongBodyLabel(label, self)
        unitWidget = StrongBodyLabel(unit, self)

        spinBox = SpinBox()
        spinBox.setMinimum(minn)
        spinBox.setMaximum(maxn)
        spinBox.setValue(value)
        spinBox.valueChanged.connect(valueChanged)

        self.hBoxLayout.addWidget(labelWidget, 0)
        self.hBoxLayout.addWidget(spinBox, 1)
        self.hBoxLayout.addWidget(unitWidget, 2)
        self.hBoxLayout.setContentsMargins(0,0,0,0)

