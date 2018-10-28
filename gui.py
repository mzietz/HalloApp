#!/usr/bin/env python


import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QFont 
from PyQt5.QtCore import QProcess
from library import *


class Flashcards(QWidget):
    
    def __init__(self, Library):
        super().__init__()        
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.library = Library
        self.initUI()
        
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Vocab trainer')    
        self.createTable()
        
        AddCardButton = QPushButton("Add Card")
        LoadDeckButton = QPushButton("Load Deck")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(AddCardButton)
        hbox.addWidget(LoadDeckButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.tableWidget)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)


    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.library.deck))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0, QTableWidgetItem(self.library.deck[0].name))
        self.tableWidget.setItem(1,0, QTableWidgetItem(self.library.deck[1].name))
        self.tableWidget.setItem(0,1, QTableWidgetItem(str(len(self.library.deck[0].card))))
        self.tableWidget.setItem(1,1, QTableWidgetItem(str(len(self.library.deck[1].card))))

        self.tableWidget.doubleClicked.connect(self.on_click)

    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
 


if __name__=="__main__":

	print ("Starting")
	app = QApplication(sys.argv)
	myLibrary = Library()
	myLibrary.loadLibrary()
	w = Flashcards(myLibrary)
	w.show()
	sys.exit(app.exec_())