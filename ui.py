from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Form(QWidget):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)

		timerLabel = QLabel("00:00")		# Might have to change data type here
		timerLabel.setObjectName("timerLabel")

		infoLabel = QLabel("No tea selected")
		infoLabel.setObjectName("infoLabel")

		banchaButton = QPushButton("Premium\nBancha")
		banchaButton.setObjectName("banchaButton")

		senchaButton = QPushButton("Premium\nSencha")
		senchaButton.setObjectName("senchaButton")

		# self.banchaButton.clicked.connect(self.submitContact)		# Event Handler
		# self.senchaButton.clicked.connect(self.submitContact)		# Event Handler

		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(6, 6, 6, 6)
		grid.addWidget(timerLabel, 0, 0, 1, 2, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		grid.addWidget(infoLabel, 1, 0, 1, 2, Qt.AlignHCenter)
		grid.addWidget(banchaButton, 2, 0)
		grid.addWidget(senchaButton, 2, 1)
		# grid.addLayout(buttonLayout1, 0, 1)

		self.setStyleSheet(open("style.qss", "r").read())		# self.setStyleSheet("* {color: red}")
		self.resize(690, 435)

		# Deprecated (sure?) style attributes
		# self.setWindowOpacity(0.85)
		# self.setWindowTitle("TeaTimer Premium")

	# def submitContact(self):
		# name = self.nameLine.text()

		# if name == "":
		# 	QMessageBox.information(self, "Empty Field",
		# 							"Please enter a name and address.")
		# 	return
		# else:
		# 	QMessageBox.information(self, "Success!",
		# 							"Hello %s!" % name)

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