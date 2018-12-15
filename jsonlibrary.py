#!/usr/bin/env python

from os.path import exists
from operator import itemgetter, attrgetter
from random import shuffle
import json

class Library:
	def __init__(self):
		self.currentCard = 0	
	def loadJSON(self):
		with open("data/library2.json") as fd:
			self.library = json.load(fd)
	def saveLibrary(self):
		with open("data/library.json", 'w') as fd:
			json.dump(self.library, fd)
			
	def nextCard(self):
		while True:
			for x in self.library:
				if x["learned"] == False:
					self.currentCard = self.library.index(x)
					return x
	def cardsLeft(self):
		i=0
		for x in self.library:
			if x["learned"] == False:
				i+=1	
		return i

	def iknowCard(self):
		self.library[self.currentCard]["learned"] = True
	def idontknowCard(self):
		self.library.append(self.library[self.currentCard])
		self.library[-1]["learned"] = False
		self.library.pop(self.currentCard)
#		self.library[self.currentCard]["learned"] = False

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadJSON()
	print(myLibrary.cardsLeft())
#	myLibrary.idontknowCard()
#	myLibrary.nextCard()
#	print(myLibrary.library)
#	myLibrary.saveLibrary()
