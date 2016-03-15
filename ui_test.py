#!/usr/bin/python3
# -*- coding: utf-8 -*-

## A simple tea timer for the brewery of excellent tea
__author__ = "Michael Knierim"

## ===========================
## IMPORTS

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

## ===========================
## CONSTANTS

WINDOW_WIDTH = 690
WINDOW_HEIGHT = 435


class WindowTitleBar(QWidget):
	def __init__(self, parent=None):
		# print("WindowTitleBar constructor gets called")
		super().__init__()

		self.setFixedHeight(32)				# This is supposed to set the container height for the title bar

		self.barTitle = QLabel(self)
		self.barTitle.setStyleSheet("color: white; font-family: Sans; font-weight: bold; font-size: 14px")

		self.windowPos = QPoint()		# Stores data relevant to the movement/deplacement of the window


	# Overloading the resizeEvent method
	# This is done so that the window is only drawn anew when a resize event occurs (so not the whole time)
	def resizeEvent(self, QResizeEvent):
		# print("WindowTitleBar resizeEvent gets called")
		self.cache = None																			# Remove old cache
		self.cache = QPixmap(self.size())											# Create a cache with same size as the widget
		self.cache.fill(Qt.transparent)												# Create the transparent background

		painter = QPainter(self.cache)												# Start painting the cache

		barBackCol = QBrush(QColor(23,23,34))
		barButtonCol = QBrush(QColor(23,63,64))

		# Title bar's frame
		framePoints = [QPoint(4,4),
									 QPoint(self.width() - 4,4),
									 QPoint(self.width() - 4,32),
									 QPoint(4,32)]
		frame = QPolygon(framePoints)

		painter.setBrush(barBackCol)
		painter.setPen(Qt.NoPen)
		painter.drawPolygon(frame)

		# Title bar's buttons area
		buttonPoints = [QPoint(self.width() - 80,  4),
										QPoint(self.width() -  4,  4),
										QPoint(self.width() -  4, 32),
										QPoint(self.width() - 80, 32)]
		buttons = QPolygon(buttonPoints)

		painter.setBrush(barButtonCol)
		painter.setPen(Qt.NoPen)
		painter.drawPolygon(buttons)

		self.barTitle.move(28,4)
		self.barTitle.resize(self.width() - 116, 29)


	# Overloading the paintEvent method
	def paintEvent(self, QPaintEvent):
		# print("WindowTitleBar paintEvent gets called")
		if self.cache != None:
			painter = QPainter(self)
			painter.drawPixmap(0, 0, self.cache)


	# Slot for keeping title synchronized. Get's called by signal WindowTitleChanged()
	def updateWindowTitle(self, titleText=""):
		self.barTitle.setText(titleText)

	# Overload mouseEvent handlers to make window moveable
	def mousePressEvent(self, QMouseEvent):
		self.windowPos = QMouseEvent.pos()
		self.setCursor(QCursor(Qt.SizeAllCursor))

	def mouseReleaseEvent(self, QMouseEvent):
		self.setCursor(QCursor(Qt.ArrowCursor))

	def mouseMoveEvent(self, QMouseEvent):
		pos = QPoint(QMouseEvent.globalPos())
		self.window().move(pos - self.windowPos)			# Why does self.window() return the Form object here? Why does this not happen in updateWindowTitle?



class Form(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		# # Instantiate custom window title bar
		self.titleBar = WindowTitleBar()						#	Instantiate

		self.windowTitleChanged.connect(self.titleBar.updateWindowTitle)
		# QObject.connect(self, SIGNAL(WindowTitleChanged()),
		#									WindowTitleBar, SLOT(UpdateWindowTitle()))		# In PyQt4, QObject.connect() is no longer implemented

		self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.setWindowTitle("Tutorial Qt: CustomWindow")

		# # Declare and specify UI elements
		# self.timerLabel = QLabel("00:00")		# Might have to change data type here
		# self.timerLabel.setObjectName("timerLabel")

		# self.infoLabel = QLabel("No tea selected")
		# self.infoLabel.setObjectName("infoLabel")

		# self.exitButton = QPushButton("x")
		# self.exitButton.setObjectName("exitButton")
		# self.exitButton.clicked.connect(QCoreApplication.instance().quit)

		# # Arrange UI elements in a layout
		grid = QGridLayout()
		grid.setSpacing(0)														# Spacing between widgets - does not work if window is resized
		self.setLayout(grid)													# Set the QGridLayout as the window's main layout
		grid.setContentsMargins(0, 0, 0, 0)
		grid.addWidget(self.titleBar, 0, 0, 1, 1)			# Put title bar in layout on top
		grid.setRowStretch(1, 1)											# Put the title bar at the top of the window
		# grid.addWidget(self.exitButton, 1, 0, 1, 2, Qt.AlignRight)
		# grid.addWidget(self.timerLabel, 2, 0, 1, 2, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		# grid.addWidget(self.infoLabel, 3, 0, 1, 2, Qt.AlignHCenter)

		# self.setStyleSheet(open("style.qss", "r").read())		# self.setStyleSheet("* {color: red}")


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


	# # In order of keeping custom title in synch with the main window, setWindowTitle is overloaded
	# def setWindowTitle(self, title):
	# 		print("gets called")
	# 		QWidget.setWindowTitle(title)
	# 		# self.WindowTitleChanged().emit()


	# Overloading the paintEvent method - However this might just be necessary in order to change the background color
	# !!! Therefore it might actually not be necessary later...
	def paintEvent(self, QPaintEvent):
		painter = QPainter(self)

		mainBackCol = QBrush(QColor(100,23,34))

		painter.setBrush(mainBackCol)
		painter.setPen(Qt.NoPen) 																# No stroke
		painter.drawRect(0, 0, self.width(), self.height())


## ===========================
## MAIN LOOP
if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)

	screen = Form()

	# Next line removes the title bar. For additional information see:
	# 		http://doc.qt.io/qt-5/qt.html#WindowType-enum
	#			http://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
	# screen.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
	screen.setWindowFlags(Qt.FramelessWindowHint)
	screen.show()

	sys.exit(app.exec_())		# Event handling loop for the application; The sys.exit() method ensures a clean exit, releasing memory resources