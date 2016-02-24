#!/usr/bin/python3
# -*- coding: utf-8 -*-

## A simple tea timer for the brewery of excellent tea
__author__ = "Michael Knierim"

import time
import data

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class QTeaButton(QPushButton):

	def __init__(self, text, parent=None):
		super().__init__(text, parent)

		# print(QPushButton.__doc__)
		# print()


class Form(QWidget):

	def __init__(self, parent=None):
		super().__init__()

		self.init_UI()


	def init_UI(self):
		# Process variables - They change with user input decisions
		self.infusionCycle = 0		# Variable to keep track of current infusion cycle (Integer)
		self.currentTea = None		# Variable to keep track of current chosen tea (Object)
		self.cTimerValue = 0			# Variable to keep track of remaining seconds in timer (Integer)

		# Declare and specify UI elements
		self.timerLabel = QLabel("00:00")		# Might have to change data type here
		self.timerLabel.setObjectName("timerLabel")

		self.infoLabel = QLabel("No tea selected")
		self.infoLabel.setObjectName("infoLabel")

		self.teaOneButton = QTeaButton(data.TEAONE.kind)
		self.teaOneButton.setObjectName("teaOneButton")
		self.teaOneButton.clicked.connect(self.prepare_infusion)		# Event Handler

		self.teaTwoButton = QTeaButton(data.TEATWO.kind)
		self.teaTwoButton.setObjectName("teaTwoButton")
		self.teaTwoButton.clicked.connect(self.prepare_infusion)		# Event Handler

		self.resetButton = QTeaButton("Reset")
		self.resetButton.setObjectName("resetButton")
		self.resetButton.hide()
		self.resetButton.clicked.connect(self.reset)		# Event Handler

		self.exitButton = QTeaButton("x")
		self.exitButton.setObjectName("exitButton")
		self.exitButton.clicked.connect(QCoreApplication.instance().quit)

		self.cTimer = QTimer(self)		# Add continous timer for infusion countdown
		self.cTimer.timeout.connect(self.countdown)

		self.sTimer = QTimer(self)		# Add single-shot timer for infusion cycle collection (preparation of infusion)
		self.sTimer.setSingleShot(True)
		self.sTimer.timeout.connect(self.infusion)

		# Arrange UI elements in a layout
		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(4, 4, 4, 4)
		grid.addWidget(self.exitButton, 0, 0, 1, 2, Qt.AlignRight)
		grid.addWidget(self.timerLabel, 1, 0, 1, 2, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		grid.addWidget(self.infoLabel, 2, 0, 1, 2, Qt.AlignHCenter)
		grid.addWidget(self.teaOneButton, 3, 0)
		grid.addWidget(self.teaTwoButton, 3, 1)
		grid.addWidget(self.resetButton, 3, 0, 1, 2)

		self.setStyleSheet(open("style.qss", "r").read())		# self.setStyleSheet("* {color: red}")
		self.resize(690, 435)


	def prepare_infusion(self):
		self.currentTea = self.sender()

		self.sTimer.start(1000)		# !!! Shorter interval check because clicks might happen fast

		self.increase_infusion_cycle()

		self.timerLabel.setText("--:--")
		displayText = self.currentTea.text().replace("\n", " ") + " - Cycle " + str(self.infusionCycle)
		self.infoLabel.setText(displayText)


	def infusion(self):
		self.teaOneButton.hide()
		self.teaTwoButton.hide()
		self.resetButton.show()

		# Start the infusion process (i.e. the countdown)
		self.cTimerValue = 90
		self.countdown()
		self.cTimer.start(1000)


	def reset(self):
		self.infusionCycle = 0
		self.cTimer.stop()

		self.timerLabel.setText("00:00")
		self.infoLabel.setText("No tea selected")

		self.teaOneButton.show()
		self.teaTwoButton.show()
		self.resetButton.hide()


	def increase_infusion_cycle(self):
		if self.infusionCycle < 3:
			self.infusionCycle += 1

		#	Reset the infusion cycle if the button is clicked a fourth time
		else:
			self.infusionCycle = 1


	def countdown(self):
		if self.cTimerValue != 0:

			minutes = self.cTimerValue // 60
			seconds = self.cTimerValue % 60

		 	# Use python string formatting to format in leading zeros
			output_string = "{0:02}:{1:02}".format(minutes, seconds)

			self.timerLabel.setText(output_string)
			self.cTimerValue -= 1
		else:
			self.reset()
			# QCoreApplication.instance().quit()		# For development purposes only


## ===========================
## MAIN LOOP
if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)

	screen = Form()

	# Next line removes the title bar. For additional information see:
	# 		http://doc.qt.io/qt-5/qt.html#WindowType-enum
	#			http://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
	screen.setWindowFlags(Qt.CustomizeWindowHint)
	screen.show()

	sys.exit(app.exec_())		# Event handling loop for the application; The sys.exit() method ensures a clean exit, releasing memory resources