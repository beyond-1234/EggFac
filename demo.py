# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt, QLocale, QTranslator
from PyQt5.QtWidgets import QApplication

from app.view.main_window import MainWindow


# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# create main window
w = MainWindow()
w.show()

app.exec_()
