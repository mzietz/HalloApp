#!/usr/bin/env python


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QGridLayout)
from PyQt5.QtGui import (QFont, QColor) 
from PyQt5.QtCore import QProcess
from library import *
import random

class Flashcards(QWidget):
    
    def __init__(self, Library):
        super().__init__()        
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 200
        self.library = Library
        self.initUI()
        
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Vocab trainer')    
        self.layout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.vlayout = QVBoxLayout()
        self.deckWindow()
        self.currentDeck = 0
        self.currentCard = 0
        self.addQuestion = ""
        self.addAnswer = ""
        self.vlayout.addLayout(self.layout)
        self.vlayout.addStretch(1)
        self.vlayout.addLayout(self.buttonLayout)
        self.setLayout(self.vlayout)

    def deckWindow(self):
        self.clear()
        self.library.saveLibrary()
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)
        self.tableWidget.setRowCount(len(self.library.deck))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setMinimumHeight(170)
        self.tableWidget.setMinimumWidth(400)
        self.tableWidget.setItem(1, 1, QTableWidgetItem())
        self.tableWidget.item(1, 1).setBackground(QtGui.QColor(0,150,150))
        self.tableWidget.setItem(1,1, QtWidgets.QTableWidgetItem())
        self.tableWidget.item(1,1).setBackground(QtGui.QColor(125,125,125))
        self.layout.addStretch(1)
   #     self.vlayout.addLayout(self.layout)
  #      self.vlayout.addStretch(1)
 #       self.vlayout.addLayout(self.buttonLayout)
#        self.setLayout(self.vlayout)
        d=0
        for x in self.library.deck:
            self.tableWidget.setItem(d,0, QTableWidgetItem(self.library.deck[d].name))
            self.tableWidget.setItem(d,1, QTableWidgetItem("Learn"))
            self.tableWidget.setItem(d,2, QTableWidgetItem("Add Card"))
            d+=1
        self.tableWidget.clicked.connect(self.on_click_deck)

    def on_click_deck(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.currentDeck = currentQTableWidgetItem.row()
            if currentQTableWidgetItem.text() == "Add Card":
                self.addCardWindow(self.currentDeck)
            if currentQTableWidgetItem.text() == "Learn":
                self.trainerWindow(self.currentDeck)

    def clear(self):
        for i in reversed(range(self.layout.count())):
            try: 
                self.layout.itemAt(i).widget().setParent(None)
            except:
                pass
        for i in reversed(range(self.vlayout.count())):
            try: 
                self.vlayout.itemAt(i).widget().setParent(None)
            except:
                pass
        for i in reversed(range(self.buttonLayout.count())):
            try: 
                self.buttonLayout.itemAt(i).widget().setParent(None)
            except:
                pass

    def trainerWindow(self, deck):
        self.clear()
#        print("trainer")
        self.library.deck[self.currentDeck].sortDeck()
        self.library.deck[self.currentDeck].shuffleDeck()
        self.questionWidget = QLabel(self.library.deck[deck].card[0].question)
        self.answerWidget = QLabel(self.library.deck[deck].card[0].answer)
        self.vlayout.insertWidget(0,self.questionWidget)
        self.cancelButton = QPushButton("Cancel!")
        self.showAnswerButton = QPushButton("Show Answer!")
        self.vlayout.addWidget(self.showAnswerButton)
        self.vlayout.addWidget(self.cancelButton)        
        self.cancelButton.clicked.connect(self.on_click_cancel)
        self.showAnswerButton.clicked.connect(self.on_click_showAnswer)

    def on_click_iknow(self):
#        print("i Know")
        source = self.sender()
        if source.text() == "Keine Ahnung":
            self.library.deck[self.currentDeck].card[0].learnedStatus=1                
        elif source.text() == "Leise Ahnung":
            self.library.deck[self.currentDeck].card[0].learnedStatus=2  
        elif source.text() == "Gerade so":
            self.library.deck[self.currentDeck].card[0].learnedStatus=3
        elif source.text() == "Easy Peasy":
            self.library.deck[self.currentDeck].card[0].learnedStatus=4
''        print(self.library.deck[self.currentDeck].card[0].learnedStatus)
        self.trainerWindow(self.currentDeck)

    def on_click_showAnswer(self):
        self.layout.removeWidget(self.showAnswerButton)
        self.showAnswerButton.deleteLater()
        self.showAnswerButton = None
        self.layout.removeWidget(self.cancelButton)
        self.cancelButton.deleteLater()
        self.cancelButton = None
        self.vlayout.insertWidget(1, self.answerWidget)
        self.a1Button = QPushButton("Keine Ahnung")
        self.a2Button = QPushButton("Leise Ahnung")
        self.a3Button = QPushButton("Gerade so")
        self.a4Button = QPushButton("Easy Peasy")
        self.buttonLayout.addWidget(self.a1Button)
        self.buttonLayout.addWidget(self.a2Button)
        self.buttonLayout.addWidget(self.a3Button)
        self.buttonLayout.addWidget(self.a4Button)
        self.a1Button.clicked.connect(self.on_click_iknow)
        self.a2Button.clicked.connect(self.on_click_iknow)
        self.a3Button.clicked.connect(self.on_click_iknow)
        self.a4Button.clicked.connect(self.on_click_iknow)
    
    def on_click_cancel(self):
#        print("Cancel")
        self.deckWindow()


    def addCardWindow(self, deck):
        self.clear()
        question = QLabel('Question')
        answer = QLabel('Answer')
        self.questionEdit = QLineEdit()
        self.answerEdit = QLineEdit()
        self.layout.setSpacing(10)
        self.layout.addWidget(question)
        self.layout.addWidget(self.questionEdit)
        self.layout.addWidget(answer)
        self.layout.addWidget(self.answerEdit)
        self.submitButton = QPushButton("Add CArd!")
        self.submitButton.clicked.connect(self.on_click_addCard)
        self.cancelButton = QPushButton("Cancel!")
        self.cancelButton.clicked.connect(self.on_click_cancel)
        self.vlayout.addWidget(self.submitButton)
        self.vlayout.addWidget(self.cancelButton) 
        # setIcon

    def on_click_addCard(self):
#        print("add Card")
        self.library.deck[self.currentDeck].addCard()
        self.library.deck[self.currentDeck].card[-1].question = self.questionEdit.text()
        self.library.deck[self.currentDeck].card[-1].answer = self.answerEdit.text()
        self.library.deck[self.currentDeck].card[-1].learnedStatus = 0
        print("Q: " +self.library.deck[self.currentDeck].card[-1].question)
        print("A: " +self.library.deck[self.currentDeck].card[-1].answer)
        print("2: " +str(self.library.deck[self.currentDeck].card[-1].learnedStatus))
        self.addCardWindow(self.currentDeck)

if __name__=="__main__":

	print ("Starting")
	app = QApplication(sys.argv)
	myLibrary = Library()
	myLibrary.loadLibrary()
	w = Flashcards(myLibrary)
	w.show()
	sys.exit(app.exec_())