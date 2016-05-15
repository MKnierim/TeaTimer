#!/usr/bin/python3
# -*- coding: utf-8 -*-

## A delightful tea timer for the brewery of excellent tea

__author__ = "Michael T. Knierim"


## IMPORTS
## ===============================================================

import time
import data

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


## CLASSES
## ===============================================================

# Customized QLabel with built-in transparency effect
class ExtendedLabel(QLabel):

    def __init__(self, text=""):
        super().__init__(text)

        # Add an opacity property to every button instance - makes it animatable later
        self.fadeEffect = QGraphicsOpacityEffect(self)
        self.fadeEffect.setOpacity(1.0)
        self.setGraphicsEffect(self.fadeEffect)

        # Add an Animation to the object
        self.Anim = QPropertyAnimation(self.fadeEffect, b"opacity")


# Customized QPushButton that does not allow to move main window while mouse is moved on top of the button
class ExtendedButton(QPushButton):

    def __init__(self, text=""):
        super().__init__(text)

    # This event function is overloaded in order to avoid the widget from delegating the event up to the parent.
    # This way, the pre-existing functionality is skipped, i.e. the window can no longer be moved while hovering over a button.
    #
    # Actually, it might also be, that there is no pre-existing functionality which might be why it didn't help to
    # set QMouseEvent.ignore()..
    def mouseMoveEvent(self, QMouseEvent):
        pass


# Customized QStackedWidget that allows transparency animations in stack changes
class ExtendedStackedWidget(QStackedWidget):

    def __init__(self, parent = None):
        QStackedWidget.__init__(self, parent)

    def setCurrentIndex(self, index):
        self.faderWidget = FaderWidget(self.currentWidget(), self.widget(index))
        QStackedWidget.setCurrentIndex(self, index)


# Customized QWidget that gives widgets a transparency fade feature
class FaderWidget(QWidget):

    def __init__(self, old_widget, new_widget):
        QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        self.old_pixmap.fill(Form.currentBackgroundColor)
        old_widget.render(self.old_pixmap, flags=QWidget.DrawChildren)
        self.pixmap_opacity = 1.0

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(200)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


# Main widget
class Form(QWidget):

    ### Constants
    ### -------------------------------------------------------------------
    WINDOW_WIDTH = 690
    WINDOW_HEIGHT = 435
    STARTCOLOR = QColor(245, 255, 206, 255)
    ENDCOLOR = QColor(201, 246, 33, 255)
    currentBackgroundColor = STARTCOLOR

    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        ### Process variables
        ### -------------------------------------------------------------------
        self.infusionCycle = 0              # Keep track of current infusion cycle (Integer)
        self.currentTea = None              # Keep track of current chosen tea (Object)
        self.countdownTimerValue = 0        # Keep track of remaining seconds in timer (Integer) - TODO Could it not also work to set a continous timer?

        # TODO Make this simpler and apply naming conventions
        self.REDCHANNELDIFF = Form.STARTCOLOR.red() - Form.ENDCOLOR.red()
        self.GREENCHANNELDIFF = Form.STARTCOLOR.green() - Form.ENDCOLOR.green()
        self.BLUECHANNELDIFF = Form.STARTCOLOR.blue() - Form.ENDCOLOR.blue()
        self.realCurrentBackgroundColor = [245.0, 255.0, 206.0, 255]        # Necessary in order to store precise rgb values - I should also check out QRgba64 objects - they might include what I need
        self.mainPalette = QPalette()
        self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)
        self.changeValue = 1.0

        ### UI elements
        ### -------------------------------------------------------------------
        self.timerLabel = ExtendedLabel("00:00")
        self.timerLabel.setObjectName("timerLabel")

        self.infoLabel = ExtendedLabel("Select your tea")
        self.infoLabel.setObjectName("infoLabel")

        # Load tea leaves image that are to be shown before and after infusion
        self.leavesLabel = ExtendedLabel()
        self.leavesLabel.setObjectName("leavesLabel")
        self.leavesLabel.setPixmap(QPixmap('resources/imgs/leaves.png'))

        # Instantiate buttons on the bottom of the app
        self.teaOneButton = ExtendedButton(data.TEAONE.name)
        self.teaOneButton.setObjectName("teaOneButton")
        self.teaOneButton.clicked.connect(self.prepareInfusion)

        self.teaTwoButton = ExtendedButton(data.TEATWO.name)
        self.teaTwoButton.setObjectName("teaTwoButton")
        self.teaTwoButton.clicked.connect(self.prepareInfusion)

        self.resetButton = ExtendedButton("Reset")
        self.resetButton.setObjectName("resetButton")
        self.resetButton.hide()
        self.resetButton.clicked.connect(self.reset)

        # Instantiate buttons on the top of the app
        self.minButton = ExtendedButton()
        self.minButton.setObjectName("minButton")
        self.minButton.clicked.connect(self.showMinimized)

        self.menuButton = ExtendedButton()
        self.menuButton.setObjectName("menuButton")
        self.menuButton.clicked.connect(self.teaMenu)

        self.exitButton = ExtendedButton()
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)

        # Tea change menu widgets
        # TODO Figure out how to make button groups or something similar here
        self.teaOneName = QLineEdit(data.TEAONE.name)
        self.teaOneCycleOne = QSpinBox()
        self.teaOneCycleOne.setRange(0, 86400)
        self.teaOneCycleOne.setValue(data.TEAONE.infusion_times[0])
        self.teaOneCycleTwo = QSpinBox()
        self.teaOneCycleTwo.setRange(0, 86400)
        self.teaOneCycleTwo.setValue(data.TEAONE.infusion_times[1])
        self.teaOneCycleThree = QSpinBox()
        self.teaOneCycleThree.setRange(0, 86400)
        self.teaOneCycleThree.setValue(data.TEAONE.infusion_times[2])
        # self.teaOneName.setObjectName("teaOneName")
        # self.teaOneCycleOne.setObjectName("teaOneCycleOne")
        # self.teaOneCycleTwo.setObjectName("teaOneCycleTwo")
        # self.teaOneCycleThree.setObjectName("teaOneCycleThree")

        self.teaTwoName = QLineEdit(data.TEATWO.name)
        self.teaTwoCycleOne = QSpinBox()
        self.teaTwoCycleOne.setRange(0, 86400)
        self.teaTwoCycleOne.setValue(data.TEATWO.infusion_times[0])
        self.teaTwoCycleTwo = QSpinBox()
        self.teaTwoCycleTwo.setRange(0, 86400)
        self.teaTwoCycleTwo.setValue(data.TEATWO.infusion_times[1])
        self.teaTwoCycleThree = QSpinBox()
        self.teaTwoCycleThree.setRange(0, 86400)
        self.teaTwoCycleThree.setValue(data.TEATWO.infusion_times[2])
        # self.teaTwoName.setObjectName("teaTwoName")
        # self.teaTwoCycleOne.setObjectName("teaTwoCycleOne")
        # self.teaTwoCycleTwo.setObjectName("teaTwoCycleTwo")
        # self.teaTwoCycleThree.setObjectName("teaTwoCycleThree")

        ### ...
        ### -------------------------------------------------------------------
        # Add continous timer for infusion countdown
        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.countdown)

        # Add single-shot timer for infusion cycle collection (preparation of infusion)
        # TODO Check if I really need this timer here in the code
        self.prepTimer = QTimer(self)
        self.prepTimer.setSingleShot(True)
        self.prepTimer.timeout.connect(self.infusion)

        # Mapping buttons to tea data
        self.teaMap = {
            self.teaOneButton : data.TEAONE,
            self.teaTwoButton : data.TEATWO
        }

        ### Layouts
        ### -------------------------------------------------------------------
        # Container layout for title bar buttons
        self.topBox = QHBoxLayout()
        self.topBox.addWidget(self.minButton)
        self.topBox.addWidget(self.menuButton)
        self.topBox.addWidget(self.exitButton)

        # Container widget and layout for infusion action buttons on bottom
        self.teaButtons = QWidget()
        self.teaButtonsBox = QHBoxLayout()
        self.teaButtonsBox.setSpacing(0)
        self.teaButtonsBox.setContentsMargins(0, 0, 0, 0)
        self.teaButtonsBox.addWidget(self.teaOneButton)
        self.teaButtonsBox.addWidget(self.teaTwoButton)
        self.teaButtons.setLayout(self.teaButtonsBox)

        # Container widgets and layouts for tea change menus on bottom
        self.teaOneMenuBox = QGridLayout()
        self.teaOneMenuBox.setSpacing(4)
        self.teaOneMenuBox.setContentsMargins(4, 0, 4, 0)
        self.teaOneMenuBox.addWidget(self.teaOneName, 1, 0, 1, -1)
        self.teaOneMenuBox.addWidget(self.teaOneCycleOne, 2, 0)
        self.teaOneMenuBox.addWidget(self.teaOneCycleTwo, 2, 1)
        self.teaOneMenuBox.addWidget(self.teaOneCycleThree, 2, 2)
        self.teaOneMenu = QWidget()
        self.teaOneMenu.setObjectName("teaOneMenu")
        self.teaOneMenu.setLayout(self.teaOneMenuBox)

        self.teaTwoMenuBox = QGridLayout()
        self.teaTwoMenuBox.setSpacing(4)
        self.teaTwoMenuBox.setContentsMargins(4, 0, 4, 0)
        self.teaTwoMenuBox.addWidget(self.teaTwoName, 1, 0, 1, -1)
        self.teaTwoMenuBox.addWidget(self.teaTwoCycleOne, 2, 0)
        self.teaTwoMenuBox.addWidget(self.teaTwoCycleTwo, 2, 1)
        self.teaTwoMenuBox.addWidget(self.teaTwoCycleThree, 2, 2)
        self.teaTwoMenu = QWidget()
        self.teaTwoMenu.setObjectName("teaTwoMenu")
        self.teaTwoMenu.setLayout(self.teaTwoMenuBox)

        self.teaMenusBox = QHBoxLayout()
        self.teaMenusBox.setSpacing(4)
        self.teaMenusBox.setContentsMargins(0, 0, 0, 0)
        self.teaMenusBox.addWidget(self.teaOneMenu)
        self.teaMenusBox.addWidget(self.teaTwoMenu)

        self.teaMenus = QWidget()
        self.teaMenus.setLayout(self.teaMenusBox)

        # Stacked widget for leaf/timer display
        self.middleStack = ExtendedStackedWidget()
        self.middleStack.addWidget(self.leavesLabel)
        self.middleStack.addWidget(self.timerLabel)

        # Stacked widget for bottom bar buttons
        self.bottomStack = ExtendedStackedWidget()
        self.bottomStack.addWidget(self.teaButtons)
        self.bottomStack.addWidget(self.resetButton)
        self.bottomStack.addWidget(self.teaMenus)

        # Final arrangement of UI elements in a grid layout
        grid = QGridLayout()
        grid.setSpacing(0)      # Spacing between widgets - does not work if window is resized
        grid.setContentsMargins(4, 4, 4, 4)
        grid.addLayout(self.topBox, 0, 1, Qt.AlignRight)
        grid.addWidget(self.middleStack, 1, 0, 1, -1, Qt.AlignHCenter)
        grid.addWidget(self.infoLabel, 2, 0, 1, -1, Qt.AlignHCenter)
        grid.addWidget(self.bottomStack, 3 , 0, 1, -1)
        self.setLayout(grid)        # Set the QGridLayout as the window's main layout

        self.setPalette(self.mainPalette)
        self.setStyleSheet(open("style.qss", "r").read())
        self.resize(Form.WINDOW_WIDTH, Form.WINDOW_HEIGHT)

    ### Window Manipulation
    ### -------------------------------------------------------------------
    # Arranging window in center of the screen (on which the mouse resides) by overloading showEvent method
    def showEvent(self, QShowEvent):
        frameGeom = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGeom.moveCenter(centerPoint)
        self.move(frameGeom.topLeft())

    # Overload mouseEvent handlers to make window moveable
    def mousePressEvent(self, QMouseEvent):
        self.windowPos = QMouseEvent.pos()
        self.setCursor(QCursor(Qt.SizeAllCursor))

    # Update window position according to mouse movement
    def mouseMoveEvent(self, QMouseEvent):
        pos = QPoint(QMouseEvent.globalPos())
        self.window().move(pos - self.windowPos)

    # Revert cursor after window movement
    def mouseReleaseEvent(self, QMouseEvent):
        self.setCursor(QCursor(Qt.ArrowCursor))

    ### Animations
    ### -------------------------------------------------------------------
    # Animate leaf label to "pulse" - after countdown is finished
    def leavesLabelAnimation(self):
        self.leavesLabel.Anim.setDuration(2400)
        self.leavesLabel.Anim.setEasingCurve(QEasingCurve.InCubic)      # InBounce looks interesting as well
        self.leavesLabel.Anim.setStartValue(1.0)
        self.leavesLabel.Anim.setKeyValueAt(0.5, 0.3)
        self.leavesLabel.Anim.setEndValue(1.0)
        self.leavesLabel.Anim.setLoopCount(-1)
        self.leavesLabel.Anim.start(QAbstractAnimation.KeepWhenStopped)
        self.leavesLabel.Anim.finished.connect(self.switchToLeaves)

    # Animate timer label to "pulse" - before countdown starts
    def timerLabelAnimation(self):
        self.timerLabel.Anim.setDuration(550)
        self.timerLabel.Anim.setEasingCurve(QEasingCurve.InQuart)
        self.timerLabel.Anim.setStartValue(1.0)
        self.timerLabel.Anim.setKeyValueAt(0.5, 0.3)
        self.timerLabel.Anim.setEndValue(1.0)
        self.timerLabel.Anim.setLoopCount(2)
        self.timerLabel.Anim.start(QAbstractAnimation.KeepWhenStopped)
        self.timerLabel.Anim.finished.connect(self.switchToTimer)

    # Simple method to increase readability for middle stacked widget changes
    def switchToLeaves(self):
        self.middleStack.setCurrentIndex(0)

    # Simple method to increase readability for middle stacked widget changes
    def switchToTimer(self):
        self.middleStack.setCurrentIndex(1)

    # Simple method to increase readability for bottom stacked widget changes
    def switchToInfusion(self):
        self.bottomStack.setCurrentIndex(0)

    # Simple method to increase readability for bottom stacked widget changes
    def switchToReset(self):
        self.bottomStack.setCurrentIndex(1)

    # Simple method to increase readability for bottom stacked widget changes
    def switchToTeaMenu(self):
        self.bottomStack.setCurrentIndex(2)

    ### Program Logic - Before countdown
    ### -------------------------------------------------------------------
    # ...
    def prepareInfusion(self):
        self.prepTimer.start(1400)

        self.switchToTimer()
        self.teaChange(self.sender())      # Check if a new type of tea is to be brewed
        self.increaseInfusionCycle()
        self.countdownTimerValue = self.teaMap[self.currentTea].infusion_times[self.infusionCycle-1]
        self.changeValue = 1.0/self.countdownTimerValue

        self.timerLabel.setText(self.displayTime())
        displayText = self.currentTea.text().replace("\n", " ") + " - Cycle " + str(self.infusionCycle)
        self.infoLabel.setText(displayText)

        self.timerLabelAnimation()

    # ...
    def teaChange(self, sender):
        if not sender == self.currentTea:
            self.currentTea = sender
            self.infusionCycle = 0

    # ...
    def increaseInfusionCycle(self):
        if self.infusionCycle < 3:
            self.infusionCycle += 1

        # Reset the infusion cycle if the button is clicked a fourth time
        else:
            self.infusionCycle = 1

    # Start the infusion process (i.e. the countdown)
    def infusion(self):
        self.switchToReset()

        self.countdown()
        self.countdownTimer.start(1000)

    ### Program Logic - During countdown
    ### -------------------------------------------------------------------
    # ...
    def countdown(self):
        if self.countdownTimerValue != 0:

            output_string = self.displayTime()

            self.timerLabel.setText(output_string)
            self.countdownTimerValue -= 1

            self.adaptBackgroundColor()
        else:
            self.finish()

    # ...
    def displayTime(self):
        minutes = self.countdownTimerValue // 60
        seconds = self.countdownTimerValue % 60

        # Use python string formatting to format in leading zeros
        output_string = "{0:02}:{1:02}".format(minutes, seconds)
        return output_string

    # Compute the new background color value each second
    def adaptBackgroundColor(self):
        newRed = self.realCurrentBackgroundColor[0] - (self.REDCHANNELDIFF * self.changeValue)
        newGreen = self.realCurrentBackgroundColor[1] - (self.GREENCHANNELDIFF * self.changeValue)
        newBlue = self.realCurrentBackgroundColor[2] - (self.BLUECHANNELDIFF * self.changeValue)

        self.realCurrentBackgroundColor = [newRed, newGreen, newBlue, 255]
        Form.currentBackgroundColor = QColor(newRed, newGreen, newBlue, 255)

        self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)
        self.setPalette(self.mainPalette)

    ### Program Logic - After countdown
    ### -------------------------------------------------------------------
    # Alert the user when the tea is finished
    def finish(self):
        self.countdownTimer.stop()          # Stop the countdown timer
        self.raise_()                       # Bring window to the foreground
        self.switchToLeaves()
        self.infoLabel.setText("Get your tea on!")
        self.leavesLabelAnimation()

    # Reset the timer to it's initial state after a tea has been brewed
    def reset(self):
        self.infusionCycle = 0
        self.countdownTimer.stop()

        # TODO Maybe I could simplify this code here
        Form.currentBackgroundColor = Form.STARTCOLOR
        self.realCurrentBackgroundColor = [245.0, 255.0, 206.0, 255]
        self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)
        self.setPalette(self.mainPalette)

        # If infusion in progress
        if self.middleStack.currentIndex() != 0:
            self.switchToLeaves()
        else:
            self.leavesLabel.Anim.setLoopCount(1)     # Return to initial state

        # Reset to initial state in any case
        self.infoLabel.setText("No tea selected")
        self.switchToInfusion()

    ### Program Logic - Additional Features
    ### -------------------------------------------------------------------
    # ...
    def teaMenu(self):
        pass


## MAIN LOOP
## ===============================================================

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('resources/fonts/CaviarDreams.ttf')        # Not sure if this is the right place here

    screen = Form()

    # Next line removes the title bar. For additional information see:
    # http://doc.qt.io/qt-5/qt.html#WindowType-enum
    # http://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
    screen.setWindowFlags(Qt.FramelessWindowHint)
    screen.show()

    sys.exit(app.exec_())       # Event handling loop for the application; The sys.exit() method ensures a clean exit, releasing memory resources