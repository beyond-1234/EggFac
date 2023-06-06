# coding: utf-8
from typing import List
from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (ScrollArea, NavigationInterface, NavigationItemPosition, PopUpAniStackedWidget)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow

from .home_interface import HomeInterface
from .setting_interface import SettingInterface, cfg
from .title_bar import CustomTitleBar
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
from ..common import resource

class StackedWidget(QFrame):
    """ Stacked widget """

    currentWidgetChanged = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)))

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def setCurrentWidget(self, widget, popOut=False):
        widget.verticalScrollBar().setValue(0)
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class MainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.settingInterface = SettingInterface(self)

        self.stackWidget.addWidget(self.homeInterface)
        self.stackWidget.addWidget(self.settingInterface)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)

        signalBus.switchToSampleCard.connect(self.switchToSample)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        # home sub page
        self.homeInterface.setObjectName('homeInterface')
        self.navigationInterface.addItem(
            routeKey=self.homeInterface.objectName(),
            icon=FIF.HOME,
            text='Home',
            onClick=lambda t: self.switchTo(self.homeInterface, t),
            position=NavigationItemPosition.TOP
        )

        # setting sub page
        self.settingInterface.setObjectName('settingsInterface')
        self.navigationInterface.addItem(
            routeKey=self.settingInterface.objectName(),
            icon=FIF.SETTING,
            text='Settings',
            onClick=lambda t: self.switchTo(self.settingInterface, t),
            position=NavigationItemPosition.BOTTOM
        )

        #!IMPORTANT: don't forget to set the default route key if you enable the return button
        self.navigationInterface.setCurrentItem(
            self.settingInterface.objectName())

        self.stackWidget.currentWidgetChanged.connect(
            lambda w: self.navigationInterface.setCurrentItem(w.objectName()))
        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        StyleSheet.MAIN_WINDOW.apply(self)

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width()-46, self.titleBar.height())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(ScrollArea)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackWidget.setCurrentWidget(w)
                # w.scrollToCard(index)
