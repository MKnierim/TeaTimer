#!/usr/bin/python3
# -*- coding: utf-8 -*-

## A simple tea timer for the brewery of excellent tea
__author__ = "Michael Knierim"


## ===========================
## MODULES
# Custom data object
import data

# Custom GUI
import ui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


## ===========================
## CONSTANTS

# !!! Not sure if still necessary - Application Colors
C_PALE_GREEN = "#F5FFCE"
C_BRIGHT_GREEN = "#C9F621"
C_DARK_GREEN = "#617610"


## ===========================
## FUNCTIONS
# !!!


## ===========================
## MAIN LOOP
if __name__ == '__main__':
	import sys

	app = QApplication(sys.argv)

	screen = ui.Form()

	# Next line removes the title bar. For additional information see:
	# 		http://doc.qt.io/qt-5/qt.html#WindowType-enum
	#			http://doc.qt.io/qt-5/qtwidgets-widgets-windowflags-example.html
	screen.setWindowFlags(Qt.CustomizeWindowHint)
	screen.show()

	sys.exit(app.exec_())		# Event handling loop for the application; The sys.exit() method ensures a clean exit, releasing memory resources