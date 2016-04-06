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

class UnmoveableButton(QPushButton):
	def __init__(self, text=""):
		super().__init__(text)

	# This event function is overloaded in order to avoid the widget from delegating the event up to the parent.
	# This way, the pre-existing functionality is skipped, i.e. the window can no longer be moved while hovering over a button.
	#
	# Actually, it might also be, that there is no pre-existing functionality which might be why it didn't help to
	# set QMouseEvent.ignore()..
	def mouseMoveEvent(self, QMouseEvent):
		pass


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

		self.infoLabel = QLabel("No tea selected")
		self.infoLabel.setObjectName("infoLabel")

		self.teaOneButton = UnmoveableButton(data.TEAONE.name)
		self.teaOneButton.setObjectName("teaOneButton")
		self.teaOneButton.clicked.connect(self.prepare_infusion)		# Event Handler

		self.teaTwoButton = UnmoveableButton(data.TEATWO.name)
		self.teaTwoButton.setObjectName("teaTwoButton")
		self.teaTwoButton.clicked.connect(self.prepare_infusion)		# Event Handler

		self.resetButton = UnmoveableButton("Reset")
		self.resetButton.setObjectName("resetButton")
		self.resetButton.hide()
		self.resetButton.clicked.connect(self.reset)					# Event Handler

		self.minButton = UnmoveableButton("_")
		self.minButton.setObjectName("minButton")
		self.minButton.clicked.connect(self.showMinimized)

		self.exitButton = UnmoveableButton("x")
		self.exitButton.setObjectName("exitButton")
		self.exitButton.clicked.connect(QCoreApplication.instance().quit)

		self.cTimer = QTimer(self)		# Add continous timer for infusion countdown
		self.cTimer.timeout.connect(self.countdown)

		self.sTimer = QTimer(self)		# Add single-shot timer for infusion cycle collection (preparation of infusion)
		self.sTimer.setSingleShot(True)
		self.sTimer.timeout.connect(self.infusion)

		# Mapping buttons to tea data
		self.teaButtons = {
			self.teaOneButton : data.TEAONE,
			self.teaTwoButton : data.TEATWO
		}

		# Create container layout for title bar buttons
		barBox = QHBoxLayout()
		barBox.addWidget(self.minButton)
		barBox.addSpacing(10)
		barBox.addWidget(self.exitButton)
		barBox.addSpacing(6)

		# Arrange UI elements in a layout
		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(4, 4, 4, 4)
		grid.addLayout(barBox, 0, 1, Qt.AlignRight)
		grid.addWidget(self.timerLabel, 1, 0, 1, -1, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		grid.addWidget(self.infoLabel, 2, 0, 1, -1, Qt.AlignHCenter)
		grid.addWidget(self.teaOneButton, 3, 0)
		grid.addWidget(self.teaTwoButton, 3, 1)
		grid.addWidget(self.resetButton, 3, 0, 1, 2)

		self.setStyleSheet(open("style.qss", "r").read())
		self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

	# Arranging window in center of the screen by overloading showEvent method
	def showEvent(self, QShowEvent):
		self.centerOnScreen()


	def centerOnScreen(self):
		screen = QDesktopWidget()
		screenGeom = QRect(screen.screenGeometry(self))

		screenCenterX = screenGeom.center().x()
		screenCenterY = screenGeom.center().y()

		self.move(screenCenterX - self.width() / 2,
							screenCenterY - self.height() / 2)


	# Overload mouseEvent handlers to make window moveable
	def mousePressEvent(self, QMouseEvent):
		self.windowPos = QMouseEvent.pos()
		self.setCursor(QCursor(Qt.SizeAllCursor))


	def mouseReleaseEvent(self, QMouseEvent):
		self.setCursor(QCursor(Qt.ArrowCursor))


	def mouseMoveEvent(self, QMouseEvent):
		pos = QPoint(QMouseEvent.globalPos())
		self.window().move(pos - self.windowPos)


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
		self.teaOneButton.hide()
		self.teaTwoButton.hide()
		self.resetButton.show()

		self.countdown()
		self.cTimer.start(1000)


	# Alert the user when the tea is finished
	def finish(self):
		self.raise_()		# Bring the window to the foreground


	# Reset the timer to it's initial state after a tea has been brewed
	def reset(self):
		self.infusionCycle = 0
		self.cTimer.stop()

		self.timerLabel.setText("00:00")
		self.infoLabel.setText("No tea selected")

		self.teaOneButton.show()
		self.teaTwoButton.show()
		self.resetButton.hide()


	def tea_change(self, sender):
		if not sender == self.currentTea:
			self.currentTea = sender
			self.infusionCycle = 0


	def increase_infusion_cycle(self):
		if self.infusionCycle < 3:
			self.infusionCycle += 1

		#	Reset the infusion cycle if the button is clicked a fourth time
		else:
			self.infusionCycle = 1


	def display_time(self):
		minutes = self.cTimerValue // 60
		seconds = self.cTimerValue % 60

		# Use python string formatting to format in leading zeros
		output_string = "{0:02}:{1:02}".format(minutes, seconds)
		return output_string


	def countdown(self):
		if self.cTimerValue != 0:

			output_string = self.display_time()

			self.timerLabel.setText(output_string)
			self.cTimerValue -= 1
		else:
			self.finish()
			self.reset()


## ===============================================================
## MAIN LOOP

if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)

	screen = Form()

	# Next line removes the title bar. For additional information see:
	# http://doc.qt.io/qt-5/qt.html#WindowType-enum
	# http://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
	screen.setWindowFlags(Qt.FramelessWindowHint)
	screen.show()

	sys.exit(app.exec_())		# Event handling loop for the application; The sys.exit() method ensures a clean exit, releasing memory resources