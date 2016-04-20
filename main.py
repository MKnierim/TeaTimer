#!/usr/bin/python3
# -*- coding: utf-8 -*-

## A simple tea timer for the brewery of excellent tea
__author__ = "Michael T. Knierim"


## ===============================================================
## IMPORTS

import time
import data

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


## ===============================================================
## CONSTANTS

WINDOW_WIDTH = 690
WINDOW_HEIGHT = 435


## ===============================================================
## CLASSES

class ExtendedButton(QPushButton):
	def __init__(self, text="", opacity=1.0):
		super().__init__(text)

		# Add an opacity property to every button instance - makes it animatable later
		self.fadeEffect = QGraphicsOpacityEffect(self)
		self.fadeEffect.setOpacity(opacity)
		self.setGraphicsEffect(self.fadeEffect)


	# This event function is overloaded in order to avoid the widget from delegating the event up to the parent.
	# This way, the pre-existing functionality is skipped, i.e. the window can no longer be moved while hovering over a button.
	#
	# Actually, it might also be, that there is no pre-existing functionality which might be why it didn't help to
	# set QMouseEvent.ignore()..
	def mouseMoveEvent(self, QMouseEvent):
		pass


# class TeaButtonStack(QStackedWidget):
# 	def __init__(self):
# 		super().__init__()


class Form(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		# Process variables - They change with user input decisions
		self.infusionCycle = 0		# Keep track of current infusion cycle (Integer)
		self.currentTea = None		# Keep track of current chosen tea (Object)
		self.cTimerValue = 0		# Keep track of remaining seconds in timer (Integer)

		# Declare and specify UI elements
		self.timerLabel = QLabel("00:00")
		self.timerLabel.setObjectName("timerLabel")

		self.infoLabel = QLabel("Select your tea")
		self.infoLabel.setObjectName("infoLabel")

		# Load tea leaves image that are to be shown before and after infusion
		self.leavesLabel = QLabel()
		self.leavesLabel.setObjectName("leavesLabel")
		self.leavesLabel.setPixmap(QPixmap('resources/imgs/leaves.png'))

		# Instantiate buttons on the bottom of the app
		self.teaOneButton = ExtendedButton(data.TEAONE.name)
		self.teaOneButton.setObjectName("teaOneButton")
		self.teaOneButton.clicked.connect(self.prepare_infusion)

		self.teaTwoButton = ExtendedButton(data.TEATWO.name)
		self.teaTwoButton.setObjectName("teaTwoButton")
		self.teaTwoButton.clicked.connect(self.prepare_infusion)

		self.resetButton = ExtendedButton("Reset", opacity=0)
		self.resetButton.setObjectName("resetButton")
		self.resetButton.hide()
		self.resetButton.clicked.connect(self.reset)

		# Load top menu icon images
		# self.minIconLabel = QLabel()
		# self.minIconLabel.setObjectName("minIconLabel")
		# self.minIconLabel.setPixmap(QPixmap('resources/imgs/minIcon.png'))

		# Instantiate buttons on the top of the app
		self.minButton = ExtendedButton("_")
		self.minButton.setObjectName("minButton")
		self.minButton.clicked.connect(self.showMinimized)

		self.exitButton = ExtendedButton("x")
		self.exitButton.setObjectName("exitButton")
		self.exitButton.clicked.connect(QCoreApplication.instance().quit)

		# Add continous timer for infusion countdown
		self.cTimer = QTimer(self)
		self.cTimer.timeout.connect(self.countdown)

		# Add single-shot timer for infusion cycle collection (preparation of infusion)
		self.sTimer = QTimer(self)
		self.sTimer.setSingleShot(True)
		self.sTimer.timeout.connect(self.infusion)

		# Mapping buttons to tea data
		self.teaButtons = {
			self.teaOneButton : data.TEAONE,
			self.teaTwoButton : data.TEATWO
		}

		# Container layout for title bar buttons
		topBox = QHBoxLayout()
		topBox.addWidget(self.minButton)
		topBox.addSpacing(10)
		topBox.addWidget(self.exitButton)
		topBox.addSpacing(6)

		# # Container layout for tea buttons on bottom
		# bottomBox = QHBoxLayout()
		# bottomBox.addWidget(self.teaOneButton)
		# topBox.addSpacing(10)
		# bottomBox.addWidget(self.teaTwoButton)

		# # Create stacked layout for bottom bar buttons
		# bottomStack = QStackedLayout()
		# bottomStack.addChildLayout(bottomBox)
		# bottomStack.addWidget(self.resetButton)

		# Arrange UI elements in a layout
		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(4, 4, 4, 4)
		grid.addLayout(topBox, 0, 1, Qt.AlignRight)
		grid.addWidget(self.leavesLabel, 1, 0, 1, -1, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		grid.addWidget(self.infoLabel, 2, 0, 1, -1, Qt.AlignHCenter)
		grid.addWidget(self.teaOneButton, 3, 0)
		grid.addWidget(self.teaTwoButton, 3, 1)
		grid.addWidget(self.resetButton, 3, 0, 1, 2)

		self.setStyleSheet(open("style.qss", "r").read())
		self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)


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


	# ...
	def mouseReleaseEvent(self, QMouseEvent):
		self.setCursor(QCursor(Qt.ArrowCursor))


	# ...
	def mouseMoveEvent(self, QMouseEvent):
		pos = QPoint(QMouseEvent.globalPos())
		self.window().move(pos - self.windowPos)


	# ...
	def buttonAnimation(self):
		DURATION = 300

		self.resetButton.show()

		self.b1Anim = QPropertyAnimation(self.teaOneButton.fadeEffect, b"opacity")
		self.b1Anim.setDuration(DURATION)
		self.b1Anim.setStartValue(1.0)
		self.b1Anim.setEndValue(0)

		self.b2Anim = QPropertyAnimation(self.teaTwoButton.fadeEffect, b"opacity")
		self.b2Anim.setDuration(DURATION)
		self.b2Anim.setStartValue(1.0)
		self.b2Anim.setEndValue(0)

		self.rAnim = QPropertyAnimation(self.resetButton.fadeEffect, b"opacity")
		self.rAnim.setDuration(DURATION)
		self.rAnim.setStartValue(0)
		self.rAnim.setEndValue(1.0)

		self.tBtnAnim = QParallelAnimationGroup()
		self.tBtnAnim.addAnimation(self.b1Anim)
		self.tBtnAnim.addAnimation(self.b2Anim)
		self.tBtnAnim.addAnimation(self.rAnim)
		self.tBtnAnim.finished.connect(self.hideButtons)
		self.tBtnAnim.start(QAbstractAnimation.KeepWhenStopped)


	# ...
	def hideButtons(self):
		self.teaOneButton.hide()
		self.teaTwoButton.hide()


	# ...
	def prepare_infusion(self):
		self.sTimer.start(1250)

		self.tea_change(self.sender())		# Check if a new type of tea is to be brewed
		self.increase_infusion_cycle()
		self.cTimerValue = self.teaButtons[self.currentTea].infusion_times[self.infusionCycle-1]

		self.timerLabel.setText(self.display_time())
		displayText = self.currentTea.text().replace("\n", " ") + " - Cycle " + str(self.infusionCycle)
		self.infoLabel.setText(displayText)


	# Start the infusion process (i.e. the countdown)
	def infusion(self):
		self.buttonAnimation()

		self.countdown()
		self.cTimer.start(1000)


	# Alert the user when the tea is finished
	def finish(self):
		self.raise_()		# Bring the window to the foreground
		self.timerLabel.hide()
		self.infoLabel.setText("Get your tea on!")


	# Reset the timer to it's initial state after a tea has been brewed
	def reset(self):
		self.infusionCycle = 0
		self.cTimer.stop()

		self.timerLabel.show()
		self.timerLabel.setText("00:00")
		self.infoLabel.setText("No tea selected")

		if self.tBtnAnim.state() == QAbstractAnimation.Running:
			self.tBtnAnim.stop()

		self.teaOneButton.show()
		self.teaTwoButton.show()
		self.resetButton.hide()

		self.teaOneButton.fadeEffect.setOpacity(1.0)
		self.teaTwoButton.fadeEffect.setOpacity(1.0)
		self.resetButton.fadeEffect.setOpacity(0)


	# ...
	def tea_change(self, sender):
		if not sender == self.currentTea:
			self.currentTea = sender
			self.infusionCycle = 0


	# ...
	def increase_infusion_cycle(self):
		if self.infusionCycle < 3:
			self.infusionCycle += 1

		#	Reset the infusion cycle if the button is clicked a fourth time
		else:
			self.infusionCycle = 1


	# ...
	def display_time(self):
		minutes = self.cTimerValue // 60
		seconds = self.cTimerValue % 60

		# Use python string formatting to format in leading zeros
		output_string = "{0:02}:{1:02}".format(minutes, seconds)
		return output_string


	# ...
	def countdown(self):
		if self.cTimerValue != 0:

			output_string = self.display_time()

			self.timerLabel.setText(output_string)
			self.cTimerValue -= 1
		else:
			self.finish()
			# self.reset()


## ===============================================================
## MAIN LOOP

if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)
	QFontDatabase.addApplicationFont('resources/fonts/CaviarDreams.ttf')		# Not sure if this is the right place here

	screen = Form()

	# Next line removes the title bar. For additional information see:
	# http://doc.qt.io/qt-5/qt.html#WindowType-enum
	# http://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
	screen.setWindowFlags(Qt.FramelessWindowHint)
	screen.show()

	sys.exit(app.exec_())		# Event handling loop for the application; The sys.exit() method ensures a clean exit, releasing memory resources