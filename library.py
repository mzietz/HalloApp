#!/usr/bin/env python


class Library:
	def __init__(self):
		self.deck = []
	def loadLibrary(self):
		with open("library.txt") as f:
			d = 0 # counter for decks
			for line in f:
				if line.startswith('D:'):
					c = 0 #counter for cards
					d += 1
					line = line.replace('D:', "")			
					self.addDeck(line)
				else:
					c += 1
					self.deck[d-1].addCard()
					end = line.find(':')
					self.deck[d-1].card[c-1].question = line[:end]
					line = line[end+1:]
					end = line.find(':')
					self.deck[d-1].card[c-1].answer = line[:end]
					line = line[end+1:]
					end = line.find(':')
					self.deck[d-1].card[c-1].learnedStatus = line[:end]
					line = line[end+1:]
					end = line.find(':')
					self.deck[d-1].card[c-1].timeUntilShow = line[:end]

	def giveName(self, name):
		self.name = name
	def addDeck(self, name):
		self.deck.append(Deck(name))

class Deck:
	def __init__ (self, name):
		self.name = name
		self.card = []
	def giveNewName(self, name):
		self.name = name
	def addCard(self):
		self.card.append(Card())
	def saveDeck(self):
		pass

class Card:
	def __init__ (self):
		self.question = ""
		self.answer = ""
		self.learnedStatus = 0
		self.timeUntilShow = 0

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadLibrary()
	print (myLibrary.deck[0].name)
	print (myLibrary.deck[1].name)
	print (myLibrary.deck[1].card[1].question)
	print (myLibrary.deck[1].card[1].answer)
	print (myLibrary.deck[1].card[1].learnedStatus)
	print (myLibrary.deck[1].card[1].timeUntilShow)
