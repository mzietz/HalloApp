#!/usr/bin/env python


import sys
#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QGridLayout, QFrame)
from PyQt5.QtGui import (QFont, QColor, QIcon) 
from PyQt5.QtCore import (QProcess, QSize)
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
        self.deckWindow()
        self.currentDeck = 0
        self.currentCard = 0
        self.addQuestion = ""
        self.addAnswer = ""
        
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle('Vocab trainer')
    
        #set parameter
        self.textfont = QFont()      
        self.textfont.setPointSize(46)
        self.buttonfont = QFont()      
        self.buttonfont.setPointSize(32)    
        self.qframe = QFrame()
        self.qframe.setLineWidth(4)
        self.qframe.Shape(QFrame.HLine)
    
        #init layouts
        self.topLayout = QHBoxLayout()
        self.topLayout.addStretch(1)
        self.topLayout.addStretch(1)
        self.answerLayout = QHBoxLayout()
        self.answerLayout.addStretch(1)
        self.answerLayout.addStretch(1)
        self.buttonLayout = QHBoxLayout()
        self.vlayout = QVBoxLayout()
    
        #add layouts to  vertikal layout
        self.vlayout.addLayout(self.topLayout)
        self.vlayout.addStretch(1)
        self.vlayout.addLayout(self.answerLayout)
        self.vlayout.addStretch(1)
        self.vlayout.addLayout(self.buttonLayout)
        self.setLayout(self.vlayout)

    def deckWindow(self):
        self.clear()
        self.library.saveLibrary()
        self.tableWidget = QTableWidget()
        self.vlayout.insertWidget(1,self.tableWidget)
        self.tableWidget.setRowCount(len(self.library.deck))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setMinimumHeight(700)
        self.tableWidget.setColumnWidth(0,800)
        d=0
        for x in self.library.deck:
            self.tableWidget.setItem(d,0, QTableWidgetItem(self.library.deck[d].name))
            self.tableWidget.setItem(d,1, QTableWidgetItem("Learn"))
            self.tableWidget.setItem(d,2, QTableWidgetItem("Add Card"))
            self.tableWidget.item(d, 0).setBackground(QColor(0,100,150))
            font = self.tableWidget.font()      
            font.setPointSize(42)               
            self.tableWidget.setFont(font)            
            self.tableWidget.item(d, 1).setBackground(QColor(0,150,200))
            self.tableWidget.item(d, 2).setBackground(QColor(0,175,200))

            d+=1
        self.tableWidget.clicked.connect(self.on_click_deck)
        self.tableWidget.resizeRowsToContents()

    def on_click_deck(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.currentDeck = currentQTableWidgetItem.row()
            if currentQTableWidgetItem.text() == "Add Card":
                self.addCardWindow(self.currentDeck)
            if currentQTableWidgetItem.text() == "Learn":
                self.trainerWindow()

    def clear(self):
        #clear all widget in layout
        for i in reversed(range(self.topLayout.count())):
            try: 
                self.topLayout.itemAt(i).widget().setParent(None)
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
        for i in reversed(range(self.answerLayout.count())):
            try: 
                self.answerLayout.itemAt(i).widget().setParent(None)
            except:
                pass

    def trainerWindow(self):
        self.clear()
        #sort and shuffle deck

        self.library.deck[self.currentDeck].sortDeck()
        self.library.deck[self.currentDeck].shuffleDeck()
        
        #define widgets
        self.questionWidget = QLabel(self.library.deck[self.currentDeck].card[0].question)               
        self.questionWidget.setFont(self.textfont)
        self.questionWidget.setWordWrap(True)                   
        self.answerWidget = QLabel(self.library.deck[self.currentDeck].card[0].answer)
        self.answerWidget.setFont(self.textfont)                    
        self.statusWidget = QLabel(self.library.deck[self.currentDeck].learned)
        self.cancelButton = QPushButton("Cancel!")
        self.cancelButton.setFont(self.buttonfont)                    
        self.showAnswerButton = QPushButton("Show Answer!")
        self.showAnswerButton.setFont(self.buttonfont)
        
        #add to topLayout                    
        self.topLayout.insertWidget(1,self.questionWidget)
        self.vlayout.addWidget(self.qframe)
        self.vlayout.addWidget(self.statusWidget)
        self.vlayout.addWidget(self.showAnswerButton)
        self.vlayout.addWidget(self.cancelButton)        
        self.cancelButton.clicked.connect(self.on_click_cancel)
        self.showAnswerButton.clicked.connect(self.on_click_showAnswer)

     
    def on_click_iknow(self):
        source = self.sender()
        if source.text() == "Keine Ahnung":
            self.library.deck[self.currentDeck].card[0].learnedStatus=1                
        elif source.text() == "Leise Ahnung":
            self.library.deck[self.currentDeck].card[0].learnedStatus=2  
        elif source.text() == "Gerade so":
            self.library.deck[self.currentDeck].card[0].learnedStatus=3
        elif source.text() == "Easy Peasy":
            self.library.deck[self.currentDeck].card[0].learnedStatus=4
        self.trainerWindow()

    def on_click_showAnswer(self):
        self.vlayout.removeWidget(self.showAnswerButton)
        self.showAnswerButton.deleteLater()
        self.showAnswerButton = None
        self.vlayout.removeWidget(self.cancelButton)
        self.cancelButton.deleteLater()
        self.cancelButton = None        
        self.vlayout.removeWidget(self.statusWidget)
        self.statusWidget.deleteLater()
        self.statusWidget = None
        self.answerLayout.insertWidget(1, self.answerWidget)
        self.a1Button = QPushButton("Keine Ahnung")
        self.a2Button = QPushButton("Leise Ahnung")
        self.a3Button = QPushButton("Gerade so")
        self.a4Button = QPushButton("Easy Peasy")
        self.a1Button.setFont(self.buttonfont)                    
        self.a2Button.setFont(self.buttonfont)                    
        self.a3Button.setFont(self.buttonfont)                    
        self.a4Button.setFont(self.buttonfont)                    
        self.buttonLayout.addWidget(self.a1Button)
        self.buttonLayout.addWidget(self.a2Button)
        self.buttonLayout.addWidget(self.a3Button)
        self.buttonLayout.addWidget(self.a4Button)
        self.a1Button.clicked.connect(self.on_click_iknow)
        self.a2Button.clicked.connect(self.on_click_iknow)
        self.a3Button.clicked.connect(self.on_click_iknow)
        self.a4Button.clicked.connect(self.on_click_iknow)
    
    def on_click_cancel(self):
        self.deckWindow()

    def addCardWindow(self, deck):
        self.clear()
        question = QLabel('Question')
        answer = QLabel('Answer')
        answer.setFont(self.buttonfont)
        question.setFont(self.buttonfont)
        self.questionEdit = QLineEdit()
        self.questionEdit.setFixedHeight(150)
        self.answerEdit = QLineEdit()
        self.answerEdit.setFixedHeight(150)
        #self.topLayout.setSpacing(10)
        self.vlayout.insertWidget(0, question)
        self.vlayout.insertWidget(1, self.questionEdit)
        self.vlayout.insertWidget(2, answer)
        self.vlayout.insertWidget(3, self.answerEdit)
        self.submitButton = QPushButton("Add CArd!")
        self.submitButton.clicked.connect(self.on_click_addCard)
        self.submitButton.setFont(self.buttonfont)
        self.cancelButton = QPushButton("Cancel!")
        self.cancelButton.clicked.connect(self.on_click_cancel)
        self.cancelButton.setFont(self.buttonfont)
        self.vlayout.addWidget(self.submitButton)
        self.vlayout.addWidget(self.cancelButton) 
        # setIcon

    def on_click_addCard(self):
        self.library.deck[self.currentDeck].addCard()
        self.library.deck[self.currentDeck].card[-1].question = self.questionEdit.text()
        self.library.deck[self.currentDeck].card[-1].answer = self.answerEdit.text()
        self.library.deck[self.currentDeck].card[-1].learnedStatus = 0
        self.addCardWindow(self.currentDeck)

if __name__=="__main__":

	print ("Starting")
	app = QApplication(sys.argv)
	myLibrary = Library()
	myLibrary.loadLibrary()
	w = Flashcards(myLibrary)
	w.showFullScreen()
	sys.exit(app.exec_())