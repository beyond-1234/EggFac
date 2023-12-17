from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import (
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
    qrouter,
    ListWidget,
    FlowLayout,
    StrongBodyLabel,
)

from ..entity.task import Task
from ..entity.track import Track


class PropLineEdit(QWidget):
    """property line edit"""

    def __init__(self, parent, label, value, valueChanged, minn=1, maxn=100, unit=""):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)
        labelWidget = StrongBodyLabel(label, self)
        unitWidget = StrongBodyLabel(unit, self)

        self.spinBox = SpinBox()
        self.spinBox.setMinimum(minn)
        self.spinBox.setMaximum(maxn)
        if isinstance(value, int):
            self.spinBox.setValue(value)
        if isinstance(value, str):
            self.spinBox.setValue(int(value))
        self.spinBox.valueChanged.connect(valueChanged)

        self.hBoxLayout.addWidget(labelWidget, 0)
        self.hBoxLayout.addWidget(self.spinBox, 1)
        self.hBoxLayout.addWidget(unitWidget, 2)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

    def setValue(self, val):
        if isinstance(val, int):
            self.spinBox.setValue(val)
        if isinstance(val, str):
            self.spinBox.setValue(int(val))
