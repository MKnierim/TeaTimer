#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
teaTimer.py: A delightful tea timer for the brewery of excellent tea.

The timer offers the possibility to store to types of tea with up to three infusion times (one per
cycle). A front-end menu is provided for the user to change the stored teas and infusion times.
"""

__author__ = "Michael T. Knierim"
__email__ = "contact@michaelknierim.info"
__license__ = "MIT"


"""
IMPORTS
===============================================================
"""

# Python built-in modules
import textwrap
import pickle

# External modules
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


"""
DATA DEFINITIONS
===============================================================
"""

## Tea is Tea(String, List)
class Tea(object):
    def __init__(self, name, infusion_times):
        self.name = name
        self.infusion_times = infusion_times


"""
CLASSES
===============================================================
"""

# Customized QLabel with built-in transparency effect
class ExtendedLabel(QLabel):

    def __init__(self, text="", objectName=""):
        super().__init__(text)

        # Simplify object naming on instantiation
        self.setObjectName(objectName)

        # Add an opacity property to every button instance - makes it animatable later
        self.fadeEffect = QGraphicsOpacityEffect(self)
        self.fadeEffect.setOpacity(1.0)
        self.setGraphicsEffect(self.fadeEffect)

        # Add an Animation to the object
        self.Anim = QPropertyAnimation(self.fadeEffect, b"opacity")


# Custom QPushButton that doesn't allow to move main window while mouse is on top of the button
class ExtendedButton(QPushButton):

    def __init__(self, text="", objectName=""):
        super().__init__(text)

        # Simplify object naming on instantiation
        self.setObjectName(objectName)

    # This event function is overloaded (or created) in order to avoid the widget from delegating 
    # the event up to the parent.This way, the pre-existing functionality is skipped, i.e. 
    # the window can no longer be moved while hovering over a button.
    def mouseMoveEvent(self, QMouseEvent):
        pass


# Customized QLineEdit to pre-define appearance and functionality for several instances later
class ExtendedLineEdit(QLineEdit):

    def __init__(self, text=""):
        super().__init__(text)

        self.setAlignment(Qt.AlignCenter)   # Center content vertically and horizontally
        self.setAttribute(Qt.WA_MacShowFocusRect, False)    # Remove blue focus rectangle
        self.setMaxLength(20)


# Customized QTimeEdit to pre-define appearance and functionality for several instances later
class ExtendedTimeEdit(QTimeEdit):

    def __init__(self, time=0):
        super().__init__()

        self.setDisplayFormat("mm:ss")
        self.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)    # Remove blue focus rectangle
        self.setWrapping(True)
        self.setTime(QTime(0, time/60, time%60, 0))


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

    # Constants
    # -------------------------------------------------------------------
    WINDOW_WIDTH = 690
    WINDOW_HEIGHT = 435
    STARTCOLOR = QColor(245, 255, 206, 255)
    ENDCOLOR = QColor(201, 246, 33, 255)
    DEFAULT_TEAS = [Tea("Dummy Tea", [0,0,0]),
                    Tea("Premium\nSencha", [3, 15, 60]),
                    Tea("Premium\nBancha", [120, 180, 240])]

    currentBackgroundColor = STARTCOLOR

    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Process variables
        # -------------------------------------------------------------------
        self.infusionCycle = 0              # Track current infusion cycle
        self.currentTea = None              # Track current Tea object
        self.countdownTimerValue = 0        # Track remaining seconds in timer

        # Load tea data (by deserializing or defaulting)
        try:
            with open("data.pickle", "rb") as dataFile:
                self.teas = pickle.load(dataFile)
        except FileNotFoundError:
            self.teas = Form.DEFAULT_TEAS

        # TODO: Simplify this
        self.redChannelDelta = Form.STARTCOLOR.red() - Form.ENDCOLOR.red()
        self.greenChannelDelta = Form.STARTCOLOR.green() - Form.ENDCOLOR.green()
        self.blueChannelDelta = Form.STARTCOLOR.blue() - Form.ENDCOLOR.blue()

        # Necessary in order to store precise rgb values - Could also check out QRgba64 objects
        self.realCurrentBackgroundColor = [245.0, 255.0, 206.0, 255]
        self.mainPalette = QPalette()
        self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)
        self.changeValue = 1.0

        # Add continous timer for infusion countdown
        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.countdown)

        # Add single-shot timer for infusion cycle collection (preparation of infusion)
        # TODO Check if I really need this timer here in the code
        self.prepTimer = QTimer(self)
        self.prepTimer.setSingleShot(True)
        self.prepTimer.timeout.connect(self.infusion)

        # UI elements
        # -------------------------------------------------------------------
        self.timerLabel = ExtendedLabel("00:00", "timerLabel")
        self.infoLabel = ExtendedLabel("Select your tea", "infoLabel")

        # Load tea leaves image that are to be shown before and after infusion
        self.leavesLabel = ExtendedLabel("", "leavesLabel")
        self.leavesLabel.setPixmap(QPixmap('resources/imgs/leaves.png'))

        # Instantiate buttons on the bottom of the app
        self.teaOneButton = ExtendedButton(self.teas[1].name, "teaOneButton")
        self.teaOneButton.clicked.connect(self.prepareInfusion)

        self.teaTwoButton = ExtendedButton(self.teas[2].name, "teaTwoButton")
        self.teaTwoButton.clicked.connect(self.prepareInfusion)

        self.resetButton = ExtendedButton("Reset", "resetButton")
        self.resetButton.clicked.connect(self.reset)

        # Instantiate buttons on the top of the app
        self.minButton = ExtendedButton("", "minButton")
        self.minButton.clicked.connect(self.showMinimized)

        self.menuButton = ExtendedButton("", "menuButton")
        self.menuButton.clicked.connect(self.teaMenu)

        self.exitButton = ExtendedButton("", "exitButton")
        self.exitButton.clicked.connect(QCoreApplication.instance().quit)

        # Tea change menu widgets
        self.teaOneNameLabel = QLabel("Tea name")
        self.teaOneName = ExtendedLineEdit(self.teas[1].name)

        self.teaOneCycleLabel = QLabel("Cycle times")
        self.t1CycleOne = ExtendedTimeEdit(self.teas[1].infusion_times[0])
        self.t1CycleTwo = ExtendedTimeEdit(self.teas[1].infusion_times[1])
        self.t1CycleThree = ExtendedTimeEdit(self.teas[1].infusion_times[2])

        self.teaTwoNameLabel = QLabel("Tea name")
        self.teaTwoName = ExtendedLineEdit(self.teas[2].name)

        self.teaTwoCycleLabel = QLabel("Cycle times")
        self.t2CycleOne = ExtendedTimeEdit(self.teas[2].infusion_times[0])
        self.t2CycleTwo = ExtendedTimeEdit(self.teas[2].infusion_times[1])
        self.t2CycleThree = ExtendedTimeEdit(self.teas[2].infusion_times[2])

        # Mapping buttons to tea data
        self.teaMap = {
            self.teaOneButton : self.teas[1],
            self.teaTwoButton : self.teas[2]
        }

        # Layouts
        # -------------------------------------------------------------------
        # Container layout for title bar buttons
        self.topBox = QHBoxLayout()
        self.topBox.addWidget(self.minButton)
        self.topBox.addWidget(self.menuButton)
        self.topBox.addWidget(self.exitButton)

        # Container widget and layout for tea buttons on bottom
        self.teaButtonsBox = QHBoxLayout()
        self.teaButtonsBox.setSpacing(4)
        self.teaButtonsBox.setContentsMargins(0, 0, 0, 0)
        self.teaButtonsBox.addWidget(self.teaOneButton)
        self.teaButtonsBox.addWidget(self.teaTwoButton)

        self.teaButtons = QWidget()
        self.teaButtons.setLayout(self.teaButtonsBox)

        # Container widgets and layouts for tea menus on bottom
        self.teaOneMenuBox = QGridLayout()
        self.teaOneMenuBox.setSpacing(4)
        self.teaOneMenuBox.setContentsMargins(16, 0, 16, 0)
        self.teaOneMenuBox.addItem(QSpacerItem(10, 15, QSizePolicy.Minimum, QSizePolicy.Minimum), 0, 0)
        self.teaOneMenuBox.addWidget(self.teaOneNameLabel, 1, 0, 1, -1, Qt.AlignHCenter)
        self.teaOneMenuBox.addWidget(self.teaOneName, 2, 0, 1, -1)
        self.teaOneMenuBox.addItem(QSpacerItem(10, 15, QSizePolicy.Minimum, QSizePolicy.Minimum), 3, 0)
        self.teaOneMenuBox.addWidget(self.teaOneCycleLabel, 4, 0, 1, -1, Qt.AlignHCenter)
        self.teaOneMenuBox.addItem(QSpacerItem(15, 1, QSizePolicy.Minimum, QSizePolicy.Minimum), 5, 0)
        self.teaOneMenuBox.addWidget(self.t1CycleOne, 5, 1)
        self.teaOneMenuBox.addWidget(self.t1CycleTwo, 5, 2)
        self.teaOneMenuBox.addWidget(self.t1CycleThree, 5, 3)
        self.teaOneMenuBox.addItem(QSpacerItem(15, 1, QSizePolicy.Minimum, QSizePolicy.Minimum), 5, 4)
        self.teaOneMenuBox.addItem(QSpacerItem(10, 15, QSizePolicy.Minimum, QSizePolicy.Minimum), 6, 0)

        self.teaOneMenu = QWidget()
        self.teaOneMenu.setObjectName("teaOneMenu")
        self.teaOneMenu.setLayout(self.teaOneMenuBox)

        self.teaTwoMenuBox = QGridLayout()
        self.teaTwoMenuBox.setSpacing(4)
        self.teaTwoMenuBox.setContentsMargins(16, 0, 16, 0)
        self.teaTwoMenuBox.addItem(QSpacerItem(10, 15, QSizePolicy.Minimum, QSizePolicy.Minimum), 0, 0)
        self.teaTwoMenuBox.addWidget(self.teaTwoNameLabel, 1, 0, 1, -1, Qt.AlignHCenter)
        self.teaTwoMenuBox.addWidget(self.teaTwoName, 2, 0, 1, -1)
        self.teaTwoMenuBox.addItem(QSpacerItem(10, 15, QSizePolicy.Minimum, QSizePolicy.Minimum), 3, 0)
        self.teaTwoMenuBox.addWidget(self.teaTwoCycleLabel, 4, 0, 1, -1, Qt.AlignHCenter)
        self.teaTwoMenuBox.addItem(QSpacerItem(15, 1, QSizePolicy.Minimum, QSizePolicy.Minimum), 5, 0)
        self.teaTwoMenuBox.addWidget(self.t2CycleOne, 5, 1)
        self.teaTwoMenuBox.addWidget(self.t2CycleTwo, 5, 2)
        self.teaTwoMenuBox.addWidget(self.t2CycleThree, 5, 3)
        self.teaTwoMenuBox.addItem(QSpacerItem(15, 1, QSizePolicy.Minimum, QSizePolicy.Minimum), 5, 4)
        self.teaTwoMenuBox.addItem(QSpacerItem(10, 15, QSizePolicy.Minimum, QSizePolicy.Minimum), 6, 0)

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

    # Window Manipulation
    # -------------------------------------------------------------------
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

    # Animations
    # -------------------------------------------------------------------
    # Animate leaf label to "pulse" - after countdown is finished
    def leavesLabelAnimation(self):
        self.leavesLabel.Anim.setDuration(2400)
        self.leavesLabel.Anim.setEasingCurve(QEasingCurve.InCubic)      # InBounce looks interesting as well
        self.leavesLabel.Anim.setStartValue(1.0)
        self.leavesLabel.Anim.setKeyValueAt(0.5, 0.3)
        self.leavesLabel.Anim.setEndValue(1.0)
        self.leavesLabel.Anim.setLoopCount(-1)
        self.leavesLabel.Anim.start(QAbstractAnimation.KeepWhenStopped)
        self.leavesLabel.Anim.finished.connect(self.switchMiddleToLeaves)

    # Animate timer label to "pulse" - before countdown starts
    def timerLabelAnimation(self):
        self.timerLabel.Anim.setDuration(550)
        self.timerLabel.Anim.setEasingCurve(QEasingCurve.InQuart)
        self.timerLabel.Anim.setStartValue(1.0)
        self.timerLabel.Anim.setKeyValueAt(0.5, 0.3)
        self.timerLabel.Anim.setEndValue(1.0)
        self.timerLabel.Anim.setLoopCount(2)
        self.timerLabel.Anim.stop()     # stop in case it was running
        self.timerLabel.Anim.start(QAbstractAnimation.KeepWhenStopped)
        self.timerLabel.Anim.finished.connect(self.switchMiddleToTimer)

    # Simple method to increase readability for middle stacked widget changes
    def switchMiddleToLeaves(self):
        self.middleStack.setCurrentIndex(0)

    # Simple method to increase readability for middle stacked widget changes
    def switchMiddleToTimer(self):
        self.middleStack.setCurrentIndex(1)

    # Simple method to increase readability for bottom stacked widget changes
    def switchBottomToInfusion(self):
        self.bottomStack.setCurrentIndex(0)

    # Simple method to increase readability for bottom stacked widget changes
    def switchBottomToReset(self):
        self.bottomStack.setCurrentIndex(1)

    # Simple method to increase readability for bottom stacked widget changes
    def switchBottomToTeaMenu(self):
        self.bottomStack.setCurrentIndex(2)
        self.teaOneName.setFocus()

    # Program Logic - Before countdown
    # -------------------------------------------------------------------
    # Pre-infusion stage where time is allowed to pass for another button click specifying a
    # different infusion cycle. After time has passed, this function proceeds to call the
    # infusion stage.
    def prepareInfusion(self):
        # TODO: Here I need an early check and set for the infusion cycle.
        # In case there are no durations set for all 3 cycles of a tea,
        # there should be no advancement to the next stage

        self.setActiveTea(self.sender())
        self.setInfusionCycle()

        self.prepTimer.start(1400)

        self.countdownTimerValue = self.currentTea.infusion_times[self.infusionCycle-1]
        self.changeValue = 1.0/self.countdownTimerValue

        # Adjust GUI items
        self.timerLabel.setText(self.displayTime())
        self.infoLabel.setText(self.currentTea.name.replace("\n", " ") + " - Cycle " + str(self.infusionCycle))
        self.switchMiddleToTimer()
        self.timerLabelAnimation()

    # Change which tea is currently set as active.
    def setActiveTea(self, sender):
        sentTea = self.teaMap[sender]   # Return Tea object mapped to sender button

        # Check if tea has changed and eventually reset cycle count
        if not sentTea == self.currentTea:
            self.currentTea = sentTea
            self.infusionCycle = 0

    # Update the current infusion cycle to be executed.
    def setInfusionCycle(self):

        if self.infusionCycle < 3:
            self.infusionCycle += 1

        else:   # Reset the cycle if the button is clicked a fourth time
            self.infusionCycle = 1

        # TODO: Figure out how to check here if next infusion cycle duration is 0
        """
            Use itertools module to cycle through infusion_times
            from itertools import cycle

            # In Tea object instantiate infusionCycle = cycle(infusion_times)

            # Go through cycle until you find next valid infusion time (i.e. >0); Then set the current cycle to this
            while True:
                self.infusionCycle = cycle.next()
                if self.infusionCycle > 0:
                    break

            # TODO: This might still be simplified a bit (e.g. specifying the while condition so that I don't need the if check later)
            # TODO: Also, the cycle variables seem rather redundant here. I should reduce this.
        """

    # Start the infusion process (i.e. the countdown)
    def infusion(self):
        self.switchBottomToReset()

        self.countdown()
        self.countdownTimer.start(1000)

    # Program Logic - During countdown
    # -------------------------------------------------------------------
    # Update the countdown display in the main window during infusion.
    def countdown(self):
        if self.countdownTimerValue != 0:

            output_string = self.displayTime()

            self.timerLabel.setText(output_string)
            self.countdownTimerValue -= 1

            self.adaptBackgroundColor()
        else:
            self.finish()

    # Format the countdown value to a minute:second string for display.
    def displayTime(self):
        minutes = self.countdownTimerValue // 60
        seconds = self.countdownTimerValue % 60

        # Use python string formatting to format in leading zeros
        output_string = "{0:02}:{1:02}".format(minutes, seconds)
        return output_string

    # Compute the new background color value each second
    def adaptBackgroundColor(self):
        newRed = self.realCurrentBackgroundColor[0] - (self.redChannelDelta * self.changeValue)
        newGreen = self.realCurrentBackgroundColor[1] - (self.greenChannelDelta * self.changeValue)
        newBlue = self.realCurrentBackgroundColor[2] - (self.blueChannelDelta * self.changeValue)

        self.realCurrentBackgroundColor = [newRed, newGreen, newBlue, 255]
        Form.currentBackgroundColor = QColor(newRed, newGreen, newBlue, 255)

        self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)
        self.setPalette(self.mainPalette)

    # Program Logic - After countdown
    # -------------------------------------------------------------------
    # Alert the user when the tea is finished
    def finish(self):
        self.countdownTimer.stop()          # Stop the countdown timer
        self.raise_()                       # Bring window to the foreground
        self.switchMiddleToLeaves()
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
            self.switchMiddleToLeaves()
        else:
            self.leavesLabel.Anim.setLoopCount(1)     # Return to initial state

        # Reset to initial state in any case
        self.infoLabel.setText("No tea selected")
        self.switchBottomToInfusion()

    # Program Logic - Tea menu
    # -------------------------------------------------------------------
    # User interaction with the tea menu where the names and cycle durations can be set.
    def teaMenu(self):
        middleStackIndex = self.middleStack.currentIndex()
        bottomStackIndex = self.bottomStack.currentIndex()

        # Switch bottom stack state only when initial state is active
        if bottomStackIndex == 0 and middleStackIndex == 0:
            self.switchBottomToTeaMenu()
            self.menuButton.setProperty("active", True)
            self.style().polish(self.menuButton)    # Update for style change

        # Enter if tea menu is visible
        elif bottomStackIndex == 2:

            # Set new values
            self.teas[1].name = self.convertToLines(self.teaOneName.text())
            self.teas[1].infusion_times[0] = self.convertToSeconds(self.t1CycleOne.time())
            self.teas[1].infusion_times[1] = self.convertToSeconds(self.t1CycleTwo.time())
            self.teas[1].infusion_times[2] = self.convertToSeconds(self.t1CycleThree.time())

            self.teas[2].name = self.convertToLines(self.teaTwoName.text())
            self.teas[2].infusion_times[0] = self.convertToSeconds(self.t2CycleOne.time())
            self.teas[2].infusion_times[1] = self.convertToSeconds(self.t2CycleTwo.time())
            self.teas[2].infusion_times[2] = self.convertToSeconds(self.t2CycleThree.time())

            # Update tea buttons
            self.teaOneButton.setText(self.teas[1].name)
            self.teaTwoButton.setText(self.teas[2].name)

            # Serialize updated tea objects
            with open("data.pickle", "wb") as dataFile:
                pickle.dump(self.teas, dataFile)

            # Switch back to initial state
            self.switchBottomToInfusion()
            self.menuButton.setProperty("active", False)
            self.style().polish(self.menuButton)    # Update for style change

            # TODO: Figure out logic for input validation and efficient updating

            """
            # Pseudo-Code for tea changes through input
            if change
                (not necessary to run update functions if no changes were made)
                (here it might come in handy that QLineEdit objects have a "modified" property)
                update data
                    if not valid input
                        (here masks and validators can be set for the QLineEdit features)
                        error prompt
                    else
                        update values in data structure (every value)
                        update button captions?
            """

            # Get all the values from the input fields
            # params = dict(teaOneName = self.teaOneName.text(),
            #               t1CycleOneMin = int(self.t1CycleOneMin.text()))

    # Stub apply user changes to tea data
    def applyTeaChanges(self):
        pass

    # Stub check if a tea name was adequately specified.
    def checkTeaName(self, input):
        pass

    # Converts QTime data into sum of seconds (integer)
    def convertToSeconds(self, time):
        seconds = time.minute()*60 + time.second()
        return seconds

    # Split tea name text to multiple lines if it is too long
    def convertToLines(self, oldTeaName):
        newTeaName = "\n".join(textwrap.wrap(oldTeaName, 12))
        return newTeaName


"""
MAIN LOOP
===============================================================
"""

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('resources/fonts/CaviarDreams.ttf')

    screen = Form()

    screen.setWindowFlags(Qt.FramelessWindowHint)       # Removes the title bar
    screen.show()

    sys.exit(app.exec_())       # sys.exit() ensures a clean exit, releasing memory resources