#!/usr/bin/env python


import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem)
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
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.deckWindow()

    def deckWindow(self):
       # Create table
        self.clear()
        self.layout.addStretch(1)
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.tableWidget.setRowCount(len(self.library.deck))
        self.tableWidget.setColumnCount(1)
        d=0
        for x in self.library.deck:
            self.tableWidget.setItem(d,0, QTableWidgetItem(self.library.deck[d].name))
            d+=1
        self.tableWidget.clicked.connect(self.on_click_deck)

    def on_click_deck(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            self.trainerWindow(0)

    def on_click_iknow(self):
        print("i Know")

    def clear(self):
        for i in reversed(range(self.layout.count())):
            try: 
                self.layout.itemAt(i).widget().setParent(None)
            except:
                pass

    def trainerWindow(self, deck):
        self.clear()
        print (deck)
        self.iKnowButton = QPushButton("I Know This!")
        self.questionWidget = QLabel(self.library.deck[deck].card[0].question)
        self.answerWidget = QLabel(self.library.deck[deck].card[0].answer)
        self.layout.addWidget(self.questionWidget)
        self.layout.addWidget(self.answerWidget)
        self.layout.addWidget(self.iKnowButton)
        self.setLayout(self.layout)
        self.iKnowButton.clicked.connect(self.on_click_iknow)


if __name__=="__main__":

	print ("Starting")
	app = QApplication(sys.argv)
	myLibrary = Library()
	myLibrary.loadLibrary()
	w = Flashcards(myLibrary)
	w.show()
	sys.exit(app.exec_())