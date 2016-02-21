#!/usr/bin/python3
# -*- coding: utf-8 -*-

## A simple tea timer for the brewery of excellent tea
__author__ = "Michael Knierim"

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
import data

class Form(QWidget):
	infusionCycle = 0		# Static variable to keep track of current infusion cycle

	def __init__(self, parent=None):
		super().__init__()

		self.init_UI()

	def init_UI(self):
		# Declare and specify UI elements
		self.timerLabel = QLabel("00:00")		# Might have to change data type here
		self.timerLabel.setObjectName("timerLabel")

		self.infoLabel = QLabel("No tea selected")
		self.infoLabel.setObjectName("infoLabel")

		self.teaOneButton = QPushButton("Premium\nBancha")
		self.teaOneButton.setObjectName("teaOneButton")
		self.teaOneButton.clicked.connect(self.infusion)		# Event Handler

		self.teaTwoButton = QPushButton("Premium\nSencha")
		self.teaTwoButton.setObjectName("teaTwoButton")
		self.teaTwoButton.clicked.connect(self.infusion)		# Event Handler

		self.resetButton = QPushButton("Reset")
		self.resetButton.setObjectName("resetButton")
		self.resetButton.hide()
		self.resetButton.clicked.connect(self.abort_infusion)		# Event Handler

		self.exitButton = QPushButton("X")
		self.exitButton.setObjectName("exitButton")
		self.exitButton.clicked.connect(QCoreApplication.instance().quit)

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

	# def prepare_infusion(self):
	# 	sender = self.sender()
	# 	teaText = sender.text().replace("\n", " ")

	# 	displayText = teaText + " - Cycle " + infusionCycle
	# 	self.infoLabel.setText(displayText)

	def infusion(self):
		self.increase_infusion_cycle()

		sender = self.sender()
		teaText = sender.text().replace("\n", " ")

		displayText = teaText + " - Infusion " + str(self.infusionCycle)
		self.infoLabel.setText(displayText)

		# Wait if button is pressed again for adjusting infusion cycle
		# time.sleep(2)		# Problem here is, that the method does not finish until the time has passed

		self.teaOneButton.hide()
		self.teaTwoButton.hide()
		self.resetButton.show()

	def abort_infusion(self):
		self.infusionCycle = 0

		self.infoLabel.setText("No tea selected")
		self.teaOneButton.show()
		self.teaTwoButton.show()
		self.resetButton.hide()

	def increase_infusion_cycle(self):
		if self.infusionCycle < 3:
			self.infusionCycle += 1


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