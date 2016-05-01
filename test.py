#!/usr/bin/python3
# -*- coding: utf-8 -*-

## ===============================================================
## IMPORTS

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
	def mouseMoveEvent(self, QMouseEvent):
		pass

class Form(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.windowPos = QPoint()		# Maybe not necessary when button click and window movement are seperated

		# Declare and specify UI elements
		self.timerLabel = QLabel("00:00")		# Might have to change data type here
		self.timerLabel.setObjectName("timerLabel")

		self.infoLabel = QLabel("No tea selected")
		self.infoLabel.setObjectName("infoLabel")

		self.teaOneButton = UnmoveableButton("Tea One")
		self.teaOneButton.setObjectName("teaOneButton")
		# self.teaOneButton.clicked.connect()

		self.teaTwoButton = UnmoveableButton("Tea Two")
		self.teaTwoButton.setObjectName("teaTwoButton")

		self.teaButtons = QWidget()
		self.teaButtonsLayout = QHBoxLayout()
		self.teaButtonsLayout.addWidget(self.teaOneButton)
		self.teaButtonsLayout.addWidget(self.teaTwoButton)
		self.teaButtons.setLayout(self.teaButtonsLayout)
		self.stackLayout = QStackedLayout()
		self.stackLayout.addWidget(self.teaButtons)

		# Arrange UI elements in a layout
		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(4, 4, 4, 4)
		grid.addWidget(self.timerLabel, 0, 0, 1, -1, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		grid.addWidget(self.infoLabel, 1, 0, 1, -1, Qt.AlignHCenter)
		grid.addLayout(self.stackLayout, 2, 0, -1, -1)

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



## ===============================================================
## MAIN LOOP

if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)

	screen = Form()
	screen.setWindowFlags(Qt.FramelessWindowHint)
	screen.show()

	sys.exit(app.exec_())