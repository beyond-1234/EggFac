from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem, QFrame
from qfluentwidgets import CheckBox, ComboBox, SpinBox, LineEdit, Pivot, qrouter, ListWidget, FlowLayout, StrongBodyLabel

from ..entity.task import Task
from ..entity.track import Track

class PropComboEdit(QWidget):
    """ property combo edit """

    def __init__(self, parent, label, items, valueChanged):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)

        labelWidget = StrongBodyLabel(label, self)
        comboBox = ComboBox(self)
        comboBox.addItems(items)
        comboBox.setCurrentIndex(0)
        comboBox.currentTextChanged.connect(valueChanged)

        self.hBoxLayout.addWidget(labelWidget, 0)
        self.hBoxLayout.addWidget(comboBox, 1)
        self.hBoxLayout.setContentsMargins(0,0,0,0)

