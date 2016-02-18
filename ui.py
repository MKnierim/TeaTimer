from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Form(QWidget):
	def __init__(self, parent=None):
		super().__init__()

		self.initUI()

	def initUI(self):
		timerLabel = QLabel("00:00")		# Might have to change data type here
		timerLabel.setObjectName("timerLabel")

		infoLabel = QLabel("No tea selected")
		infoLabel.setObjectName("infoLabel")

		banchaButton = QPushButton("Premium\nBancha")
		banchaButton.setObjectName("banchaButton")
		banchaButton.clicked.connect(self.infusion)		# Event Handler

		senchaButton = QPushButton("Premium\nSencha")
		senchaButton.setObjectName("senchaButton")
		senchaButton.clicked.connect(self.infusion)		# Event Handler

		resetButton = QPushButton("Reset")
		resetButton.setObjectName("resetButton")
		resetButton.clicked.connect(self.abort_infusion)		# Event Handler
		resetButton.hide()

		exitButton = QPushButton("X")
		exitButton.setObjectName("exitButton")
		exitButton.clicked.connect(QCoreApplication.instance().quit)

		grid = QGridLayout()
		self.setLayout(grid)		# Set the QGridLayout as the window's main layout
		grid.setSpacing(0)		# Spacing between widgets - does not work if window is resized
		grid.setContentsMargins(4, 4, 4, 4)
		grid.addWidget(exitButton, 0, 0, 1, 2, Qt.AlignRight)
		grid.addWidget(timerLabel, 1, 0, 1, 2, Qt.AlignHCenter)		# http://doc.qt.io/qt-5/qgridlayout.html#addWidget
		grid.addWidget(infoLabel, 2, 0, 1, 2, Qt.AlignHCenter)
		grid.addWidget(banchaButton, 3, 0)
		grid.addWidget(senchaButton, 3, 1)
		grid.addWidget(resetButton, 3, 0, 1, 2)

		self.setStyleSheet(open("style.qss", "r").read())		# self.setStyleSheet("* {color: red}")
		self.resize(690, 435)

		# Deprecated (sure?) style attributes
		# self.setWindowOpacity(0.925)
		# self.setWindowTitle("TeaTimer Premium")

	def infusion(self):
		QMessageBox.information(self, "Yeah!", "Let's brew some tea!")

		# Manage button display
		# self.banchaButton.hide()
		# self.senchaButton.hide()
		# self.resetButton.show()

	def abort_infusion(self):
		QMessageBox.information(self, "No!", "Stop this infusion madness!")