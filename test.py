import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.label = QLabel("Test", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {background-color: red;}")

        self.button = QPushButton("Test", self)

        self.tableWidget = QTableWidget()
        
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()
#        self.tableWidget.setMinimumHeight(700)
#        self.tableWidget.setMinimumWidth(400)
#        self.tableWidget.setColumnWidth(0,80)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
        self.layout.addWidget(self.tableWidget, 1, 1)

        self.setLayout(self.layout)
        self.show()

app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())