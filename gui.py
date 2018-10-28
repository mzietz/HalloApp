#!/usr/bin/env python


import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QGridLayout)
from PyQt5.QtGui import QFont 
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
        self.setLayout(self.layout)
        self.deckWindow()
        self.currentDeck = 0
        self.currentCard = 0
        self.addQuestion = ""
        self.addAnswer = ""

    def deckWindow(self):
        self.clear()
        self.library.saveLibrary()
        self.layout.addStretch(1)
        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.tableWidget.setRowCount(len(self.library.deck))
        self.tableWidget.setColumnCount(3)
        d=0
        for x in self.library.deck:
            self.tableWidget.setItem(d,0, QTableWidgetItem(self.library.deck[d].name))
            self.tableWidget.setItem(d,1, QTableWidgetItem("Learn"))
            self.tableWidget.setItem(d,2, QTableWidgetItem("Add Card"))
            d+=1
        self.tableWidget.clicked.connect(self.on_click_deck)

    def on_click_deck(self):
#        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
#            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            self.currentDeck = currentQTableWidgetItem.row()
#            print(self.currentDeck)
            if currentQTableWidgetItem.text() == "Add Card":
                self.addCardWindow(self.currentDeck)
            if currentQTableWidgetItem.text() == "Learn":
                self.trainerWindow(self.currentDeck)

    def on_click_iknow(self):
        print("i Know")
        self.layout.addWidget(self.answerWidget)
        self.setLayout(self.layout)
        self.nextButton = QPushButton("NExt")
        self.layout.addWidget(self.nextButton)
        source = self.sender()
        if source.text() == "Keine Ahnung":
            self.library.deck[self.currentDeck].card[0].learnedStatus=1                
        elif source.text() == "Leise Ahnung":
            self.library.deck[self.currentDeck].card[0].learnedStatus=2  
        elif source.text() == "Gerade so":
            self.library.deck[self.currentDeck].card[0].learnedStatus=3
        elif source.text() == "Easy Peasy":
            self.library.deck[self.currentDeck].card[0].learnedStatus=4
        print(self.library.deck[self.currentDeck].card[0].learnedStatus)
        self.nextButton.clicked.connect(self.on_click_next)

    def on_click_next(self):
        print("next")
        self.trainerWindow(self.currentDeck)

    def on_click_addCard(self):
        print("add Card")
        self.library.deck[self.currentDeck].addCard()
        self.library.deck[self.currentDeck].card[-1].question = self.questionEdit.text()
#        print("nummer: "+"text"+self.questionEdit.text())
        self.library.deck[self.currentDeck].card[-1].answer = self.answerEdit.text()
        self.library.deck[self.currentDeck].card[-1].timeUntilShow = 0
        self.library.deck[self.currentDeck].card[-1].learnedStatus = 0
        print("Q: " +self.library.deck[self.currentDeck].card[-1].question)
        print("A: " +self.library.deck[self.currentDeck].card[-1].answer)
        print("1: " +str(self.library.deck[self.currentDeck].card[-1].timeUntilShow))
        print("2: " +str(self.library.deck[self.currentDeck].card[-1].learnedStatus))
        self.addCardWindow(self.currentDeck)
    
    def on_click_cancel(self):
        print("Cancel")
        self.deckWindow()

    def clear(self):
        for i in reversed(range(self.layout.count())):
            try: 
                self.layout.itemAt(i).widget().setParent(None)
            except:
                pass
#        print("Cleared "+str(self.layout.count()) +" objects")

    def trainerWindow(self, deck):
        self.clear()
        print("trainer")
        self.a1Button = QPushButton("Keine Ahnung")
        self.a2Button = QPushButton("Leise Ahnung")
        self.a3Button = QPushButton("Gerade so")
        self.a4Button = QPushButton("Easy Peasy")
        #self.currentCard = 0 
        self.library.deck[self.currentDeck].sortDeck()
        self.questionWidget = QLabel(self.library.deck[deck].card[0].question)
        self.answerWidget = QLabel(self.library.deck[deck].card[0].answer)
        self.layout.addWidget(self.questionWidget)
        self.layout.addWidget(self.a1Button)
        self.layout.addWidget(self.a2Button)
        self.layout.addWidget(self.a3Button)
        self.layout.addWidget(self.a4Button)
        self.setLayout(self.layout)
        self.a1Button.clicked.connect(self.on_click_iknow)
        self.a2Button.clicked.connect(self.on_click_iknow)
        self.a3Button.clicked.connect(self.on_click_iknow)
        self.a4Button.clicked.connect(self.on_click_iknow)
        self.cancelButton = QPushButton("Cancel!")
        self.cancelButton.clicked.connect(self.on_click_cancel)
        self.layout.addWidget(self.cancelButton)


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
        self.layout.addWidget(self.submitButton)
        self.layout.addWidget(self.cancelButton)
        self.setLayout(self.layout)

if __name__=="__main__":

	print ("Starting")
	app = QApplication(sys.argv)
	myLibrary = Library()
	myLibrary.loadLibrary()
	w = Flashcards(myLibrary)
	w.show()
	sys.exit(app.exec_())