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
	def __init__(self, text=""):
		super().__init__(text)

	# This event function is overloaded in order to avoid the widget from delegating the event up to the parent.
	# This way, the pre-existing functionality is skipped, i.e. the window can no longer be moved while hovering over a button.
	#
	# Actually, it might also be, that there is no pre-existing functionality which might be why it didn't help to
	# set QMouseEvent.ignore()..
	def mouseMoveEvent(self, QMouseEvent):
		pass


class ExtendedStackedWidget(QStackedWidget):
	def __init__(self, parent = None):
		QStackedWidget.__init__(self, parent)

	def setCurrentIndex(self, index):
		self.fader_widget = FaderWidget(self.currentWidget(), self.widget(index))
		QStackedWidget.setCurrentIndex(self, index)


class FaderWidget(QWidget):
	def __init__(self, old_widget, new_widget):
		QWidget.__init__(self, new_widget)

		self.old_pixmap = QPixmap(new_widget.size())
		self.old_pixmap.fill(Form.currentBackgroundColor)		# This works for now, but could be problematic later when I alter the background color
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


class Form(QWidget):
	STARTCOLOR = QColor(245, 255, 206, 255)
	ENDCOLOR = QColor(201, 246, 33, 255)
	currentBackgroundColor = STARTCOLOR

	def __init__(self, parent=None):
		super().__init__()

		# Process variables - They change with user input decisions
		self.infusionCycle = 0				# Keep track of current infusion cycle (Integer)
		self.currentTea = None				# Keep track of current chosen tea (Object)
		self.countdownTimerValue = 0		# Keep track of remaining seconds in timer (Integer)

		# !!! Make this simpler and apply naming conventions
		self.REDCHANNELDIFF = Form.STARTCOLOR.red() - Form.ENDCOLOR.red()
		self.GREENCHANNELDIFF = Form.STARTCOLOR.green() - Form.ENDCOLOR.green()
		self.BLUECHANNELDIFF = Form.STARTCOLOR.blue() - Form.ENDCOLOR.blue()
		self.realCurrentBackgroundColor = [245.0, 255.0, 206.0, 255]		# Necessary in order to store precise rgb values - I should also check out QRgba64 objects - they might include what I need
		self.mainPalette = QPalette()
		self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)

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
		# self.menuButton.clicked.connect()

		self.exitButton = ExtendedButton()
		self.exitButton.setObjectName("exitButton")
		self.exitButton.clicked.connect(QCoreApplication.instance().quit)

		# Add continous timer for infusion countdown
		self.countdownTimer = QTimer(self)
		self.countdownTimer.timeout.connect(self.countdown)

		# Add single-shot timer for infusion cycle collection (preparation of infusion)
		# !!! Check if I really need this timer here in the code
		self.prepTimer = QTimer(self)
		self.prepTimer.setSingleShot(True)
		self.prepTimer.timeout.connect(self.infusion)

		# Mapping buttons to tea data
		self.teaMap = {
			self.teaOneButton : data.TEAONE,
			self.teaTwoButton : data.TEATWO
		}

		### Layouting
		# Container layout for title bar buttons
		self.topBox = QHBoxLayout()
		self.topBox.addWidget(self.minButton)
		self.topBox.addWidget(self.menuButton)
		self.topBox.addWidget(self.exitButton)

		# Stacked widget for leaf/timer display
		self.middleStack = ExtendedStackedWidget()
		self.middleStack.addWidget(self.leavesLabel)
		self.middleStack.addWidget(self.timerLabel)

		# Container widget and layout for tea buttons on bottom
		self.teaButtons = QWidget()
		self.bottomBox = QHBoxLayout()
		self.bottomBox.setSpacing(0)
		self.bottomBox.setContentsMargins(0, 0, 0, 0)
		self.bottomBox.addWidget(self.teaOneButton)
		self.bottomBox.addWidget(self.teaTwoButton)
		self.teaButtons.setLayout(self.bottomBox)

		# Stacked widget for bottom bar buttons
		self.bottomStack = ExtendedStackedWidget()
		self.bottomStack.addWidget(self.teaButtons)
		self.bottomStack.addWidget(self.resetButton)


		# Final arrangement of UI elements in a grid layout
		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(4, 4, 4, 4)
		grid.addLayout(self.topBox, 0, 1, Qt.AlignRight)
		grid.addWidget(self.middleStack, 1, 0, 1, -1, Qt.AlignHCenter)
		grid.addWidget(self.infoLabel, 2, 0, 1, -1, Qt.AlignHCenter)
		grid.addWidget(self.bottomStack, 3 , 0, 1, -1)

		self.setPalette(self.mainPalette)
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
		# def buttonAnimation(self):
		# 	DURATION = 300

		# 	self.resetButton.show()

		# 	self.b1Anim = QPropertyAnimation(self.teaOneButton.fadeEffect, b"opacity")
		# 	self.b1Anim.setDuration(DURATION)
		# 	self.b1Anim.setStartValue(1.0)
		# 	self.b1Anim.setEndValue(0)

		# 	self.b2Anim = QPropertyAnimation(self.teaTwoButton.fadeEffect, b"opacity")
		# 	self.b2Anim.setDuration(DURATION)
		# 	self.b2Anim.setStartValue(1.0)
		# 	self.b2Anim.setEndValue(0)

		# 	self.rAnim = QPropertyAnimation(self.resetButton.fadeEffect, b"opacity")
		# 	self.rAnim.setDuration(DURATION)
		# 	self.rAnim.setStartValue(0)
		# 	self.rAnim.setEndValue(1.0)

		# 	self.tBtnAnim = QParallelAnimationGroup()
		# 	self.tBtnAnim.addAnimation(self.b1Anim)
		# 	self.tBtnAnim.addAnimation(self.b2Anim)
		# 	self.tBtnAnim.addAnimation(self.rAnim)
		# 	self.tBtnAnim.finished.connect(self.hideButtons)
		# 	self.tBtnAnim.start(QAbstractAnimation.KeepWhenStopped)


		# # ...
		# def hideButtons(self):
		# 	self.teaOneButton.hide()
		# 	self.teaTwoButton.hide()


	# ...
	def prepare_infusion(self):
		self.prepTimer.start(1250)

		self.middleStack.setCurrentIndex(1)
		self.tea_change(self.sender())		# Check if a new type of tea is to be brewed
		self.increase_infusion_cycle()
		self.countdownTimerValue = self.teaMap[self.currentTea].infusion_times[self.infusionCycle-1]

		self.timerLabel.setText(self.display_time())
		displayText = self.currentTea.text().replace("\n", " ") + " - Cycle " + str(self.infusionCycle)
		self.infoLabel.setText(displayText)


	# Start the infusion process (i.e. the countdown)
	def infusion(self):
		self.bottomStack.setCurrentIndex(1)

		self.countdown()
		self.countdownTimer.start(1000)


	# Alert the user when the tea is finished
	def finish(self):
		self.countdownTimer.stop()				# Stop the countdown timer
		self.raise_()							# Bring the window to the foreground
		self.middleStack.setCurrentIndex(0)		# Show leaf image again
		self.infoLabel.setText("Get your tea on!")


	# Reset the timer to it's initial state after a tea has been brewed
	def reset(self):
		self.infusionCycle = 0
		self.countdownTimer.stop()

		# !!! Maybe I could simplify this code here
		Form.currentBackgroundColor = Form.STARTCOLOR
		self.realCurrentBackgroundColor = [245.0, 255.0, 206.0, 255]
		self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)
		self.setPalette(self.mainPalette)

		self.infoLabel.setText("No tea selected")

		# self.timerLabel.setText("00:00")
		if self.middleStack.currentIndex() != 0:		# Show leaf image only if not yet present
			self.middleStack.setCurrentIndex(0)

		self.bottomStack.setCurrentIndex(0)

		# if self.tBtnAnim.state() == QAbstractAnimation.Running:
		# 	self.tBtnAnim.stop()


	# ...
	def test_method(self):
		pass

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
		minutes = self.countdownTimerValue // 60
		seconds = self.countdownTimerValue % 60

		# Use python string formatting to format in leading zeros
		output_string = "{0:02}:{1:02}".format(minutes, seconds)
		return output_string


	# ...
	def countdown(self):
		if self.countdownTimerValue != 0:

			output_string = self.display_time()

			self.adaptBackgroundColor()

			self.timerLabel.setText(output_string)
			self.countdownTimerValue -= 1
		else:
			self.finish()

	# This function is used to compute the new background color value each second
	def adaptBackgroundColor(self):
		changeValue = 1.0/(self.teaMap[self.currentTea].infusion_times[self.infusionCycle-1])		# Actually not necessary to calculate it here every time... could go to constructor

		newRed = self.realCurrentBackgroundColor[0] - (self.REDCHANNELDIFF * changeValue)
		newGreen = self.realCurrentBackgroundColor[1] - (self.GREENCHANNELDIFF * changeValue)
		newBlue = self.realCurrentBackgroundColor[2] - (self.BLUECHANNELDIFF * changeValue)

		self.realCurrentBackgroundColor = [newRed, newGreen, newBlue, 255]
		Form.currentBackgroundColor = QColor(newRed, newGreen, newBlue, 255)

		# print(self.realCurrentBackgroundColor)
		# print(Form.currentBackgroundColor.getRgb())
		self.mainPalette.setColor(QPalette.Background,Form.currentBackgroundColor)
		self.setPalette(self.mainPalette)


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