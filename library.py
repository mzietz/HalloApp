#!/usr/bin/env python

from operator import itemgetter, attrgetter
from random import shuffle

class Library:
	def __init__(self):
		self.deck = []
	def loadLibrary(self):
		with open("library.txt") as f:
			d = 0 # counter for decks
			for line in f:
				if line.startswith('D!'):
					c = 0 #counter for cards
					d += 1
					line = line.replace('D!', "")
					end = line.find(':')			
					self.addDeck(line[:end])
					line = line[end+1:]
					self.deck[d-1].number = line[:end]
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
					self.deck[d-1].card[c-1].learnedStatus = int(line[:end])
					line = line[end+1:]
					end = line.find(':')
					self.deck[d-1].card[c-1].timeUntilShow = int(line[:end])

	def saveLibrary(self):
#		print(self.deck[0].card[0].question+":"+self.deck[0].card[0].answer+":"+self.deck[0].card[0].learnedStatus+":"+self.deck[0].card[0].timeUntilShow)
		with open("library.txt", "w") as f:
			d=0 # counter for decks
			for x1 in self.deck:
				f.write("D!"+self.deck[d].name+":"+self.deck[d].number)
				c=0 # counter for cards
				for x2 in self.deck[d].card:
					f.write(self.deck[d].card[c].question+":"+self.deck[d].card[c].answer+":"+str(self.deck[d].card[c].learnedStatus)+":"+str(self.deck[d].card[c].timeUntilShow)+"\n")
#					print(self.deck[d].card[c].question+":"+self.deck[d].card[c].answer+":"+self.deck[d].card[c].learnedStatus+":"+self.deck[d].card[c].timeUntilShow)
					c+=1
				d+=1
		f.close()
		print("saved")
	def giveName(self, name):
		self.name = name
	def addDeck(self, name):
		self.deck.append(Deck(name))

class Deck:
	def __init__ (self, name):
		self.name = name
		self.number = 0
		self.card = []
	def giveNewName(self, name):
		self.name = name
	def addCard(self):
		self.card.append(Card())
#		self.card[-1].question = question
#		self.card[-1].answer = answer
	def sortDeck(self):
		self.card.sort(key=attrgetter('learnedStatus'))
	def shuffleDeck(self):
		i=0
		lastStatus = self.card[i].learnedStatus
		while i < 5:
			i+=1
			try:
				if self.card[i].learnedStatus != lastStatus:
					break
			except:
				break
#		self.card.shuffle()
		x=self.card[0:i]				
		shuffle(x)
		self.card[0:i] = x
		if self.card[0].learnedStatus == 4:
			print("Deck learned")

class Card:
	def __init__ (self):
		self.question = ""
		self.answer = ""
		self.learnedStatus = 0
		self.timeUntilShow = 0

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadLibrary()
	print (myLibrary.deck[1].card[0].learnedStatus)
	print (myLibrary.deck[1].card[1].learnedStatus)
	print (myLibrary.deck[1].card[2].learnedStatus)
	print (myLibrary.deck[1].card[3].learnedStatus)
#	myLibrary.saveLibrary()
	myLibrary.deck[1].sortDeck()
	print (myLibrary.deck[1].card[0].question)
	print (myLibrary.deck[1].card[1].question)
	print (myLibrary.deck[1].card[2].question)
	print (myLibrary.deck[1].card[3].question)

	myLibrary.deck[1].shuffleDeck()
#	print (myLibrary.deck[0].name)
#	print (myLibrary.deck[1].name)
#	print (myLibrary.deck[0].number)
#	print (myLibrary.deck[1].number)
	print (myLibrary.deck[1].card[0].question)
	print (myLibrary.deck[1].card[1].question)
	print (myLibrary.deck[1].card[2].question)
	print (myLibrary.deck[1].card[3].question)
	myLibrary.saveLibrary()
