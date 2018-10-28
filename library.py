#!/usr/bin/env python


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
					self.deck[d-1].card[c-1].learnedStatus = line[:end]
					line = line[end+1:]
					end = line.find(':')
					self.deck[d-1].card[c-1].timeUntilShow = line[:end]

	def saveLibrary(self):
		with open("library1.txt", "w") as f:
			d=0 # counter for decks
			for x1 in self.deck:
				f.write("D:"+self.deck[d].name+":"+self.deck[d].number)
				c=0 # counter for cards
				for x2 in self.deck[d].card:
					f.write(self.deck[d].card[c].question+":"+self.deck[d].card[c].answer+":"+self.deck[d].card[c].learnedStatus+":"+self.deck[d].card[c].timeUntilShow+"\n")
#					print(self.deck[d].card[c].question+":"+self.deck[d].card[c].answer+":"+self.deck[d].card[c].learnedStatus+":"+self.deck[d].card[c].timeUntilShow)
					c+=1
				d+=1
		f.close()
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


class Card:
	def __init__ (self):
		self.question = ""
		self.answer = ""
		self.learnedStatus = 0
		self.timeUntilShow = 0

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadLibrary()
	myLibrary.saveLibrary()
#	print (myLibrary.deck[0].name)
#	print (myLibrary.deck[1].name)
#	print (myLibrary.deck[0].number)
#	print (myLibrary.deck[1].number)
#	print (myLibrary.deck[1].card[1].question)
#	print (myLibrary.deck[1].card[1].answer)
#	print (myLibrary.deck[1].card[1].learnedStatus)
#	print (myLibrary.deck[1].card[1].timeUntilShow)
