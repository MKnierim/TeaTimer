from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Form(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.init_UI()

	def init_UI(self):
		self.timerLabel = QLabel("00:00")		# Might have to change data type here
		self.timerLabel.setObjectName("timerLabel")

		self.infoLabel = QLabel("No tea selected")
		self.infoLabel.setObjectName("infoLabel")

		self.banchaButton = QPushButton("Premium\nBancha")
		self.banchaButton.setObjectName("banchaButton")
		self.banchaButton.clicked.connect(self.infusion)		# Event Handler

		self.senchaButton = QPushButton("Premium\nSencha")
		self.senchaButton.setObjectName("senchaButton")
		self.senchaButton.clicked.connect(self.infusion)		# Event Handler

		self.resetButton = QPushButton("Reset")
		self.resetButton.setObjectName("resetButton")
		self.resetButton.hide()
		self.resetButton.clicked.connect(self.abort_infusion)		# Event Handler

		self.exitButton = QPushButton("X")
		self.exitButton.setObjectName("exitButton")
		self.exitButton.clicked.connect(QCoreApplication.instance().quit)


		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(4, 4, 4, 4)
		grid.addWidget(self.exitButton, 0, 0, 1, 2, Qt.AlignRight)
		grid.addWidget(self.timerLabel, 1, 0, 1, 2, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		grid.addWidget(self.infoLabel, 2, 0, 1, 2, Qt.AlignHCenter)
		grid.addWidget(self.banchaButton, 3, 0)
		grid.addWidget(self.senchaButton, 3, 1)
		grid.addWidget(self.resetButton, 3, 0, 1, 2)

		self.setStyleSheet(open("style.qss", "r").read())		# self.setStyleSheet("* {color: red}")
		self.resize(690, 435)

		# Deprecated (sure?) style attributes
		# self.setWindowOpacity(0.925)
		# self.setWindowTitle("TeaTimer Premium")

	def infusion(self):
		sender = self.sender()
		QMessageBox.information(self, "Yeah!", "Let's brew some %s!" % sender.text())

		self.banchaButton.hide()
		self.senchaButton.hide()
		self.resetButton.show()

	def abort_infusion(self):
		# QMessageBox.information(self, "No!", "Stop this infusion madness!")
		self.banchaButton.show()
		self.senchaButton.show()
		self.resetButton.hide()