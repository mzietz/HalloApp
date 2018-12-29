#!/usr/bin/env python

from os.path import join, exists
from operator import itemgetter, attrgetter
from random import shuffle
import json
import datetime

class Library:
	def __init__(self):
		self.currentCard = 0
		self.currentChunk = 0
		self.currentDeck = ""
		self.difficulty = 1
		self.chunkSize = 10
		self.numberOfChunks = 0
		self.date = datetime.datetime.now()

	def loadDecks(self):
		with open(join("data/", 'decks.json')) as fd:
			self.decks = json.load(fd)
	
	def saveDecks(self):
		for x in self.decks:
			if x["text"] == self.currentDeck:
				x["selected"] = True
			else:
				x["selected"] = False
		with open(join("data/", 'decks.json'), 'w') as fd:
			json.dump(self.decks, fd)
		print "decks saved!"
	
	def loadVocabs(self):
		with open(join("data/", self.currentDeck+'.json')) as fd:
			self.library = json.load(fd)
	
#	def saveVocabs(self): #for variable chunkssize only
#		with open(join("data/", 'cache.json'), 'w') as fd:
#			json.dump(self.library, fd)

	def resetLearnedStatus(self):
		for x in self.library:
			x["learned"] = False

	def saveVocabs(self):
		for x in self.library:
			if x["chunk"] == self.currentChunk:
				x["difficulty"] = self.difficulty
				x["date"] = unicode(datetime.datetime.now())
		
#		with open(join("data/", self.currentDeck+'.json'), 'w') as fd:
		with open(join("data/", self.currentDeck+'.json'), 'w') as fd:
			json.dump(self.library, fd)

			
	def nextCard(self):
		for x in self.library:
			if x["learned"] == False and x["chunk"] == self.currentChunk:
				self.currentCard = self.library.index(x)
				return x
	
	def cardsLeft(self):
		i=0
		for x in self.library:
			if x["learned"] == False and x["chunk"] == self.currentChunk:
				i+=1	
		return i

	def cardsStudied(self):
		i=0
		for x in self.library:
			if x["difficulty"] == 0:
				i+=1	
		return i

	def cardsNotStudied(self):
		i=0
		for x in self.library:
			if x["difficulty"] != False:
				i+=1	
		return i
	def nextChunk(self):

		self.date = datetime.datetime.now()
		for x in self.library:
			if x["difficulty"] > self.difficulty:
				self.difficulty = x["difficulty"]
				self.currentChunk = x["chunk"]
				
			if x["difficulty"] == self.difficulty and x["difficulty"] != 0 and datetime.datetime.strptime(x["date"], '%Y-%m-%d %X.%f') > self.date:
				self.date = datetime.datetime.strptime(x["date"], '%Y-%m-%d %X.%f')
				self.currentChunk = x["chunk"]
			
			if x["difficulty"] == 0 and datetime.datetime.strptime(x["date"], '%Y-%m-%d %X.%f') < self.date:
				self.date = datetime.datetime.strptime(x["date"], '%Y-%m-%d %X.%f')
				self.currentChunk = x["chunk"]
		self.difficulty = 0
		self.date = datetime.datetime.now()
		return self.currentChunk

	def iknowCard(self):
		self.library[self.currentCard]["learned"] = True

	def idontknowCard(self):
#		self.library[self.currentCard]["learned"] = False

		for x in self.library:
			if x["chunk"] is self.currentChunk :
				self.library.insert(self.library.index(x)+self.chunkSize,self.library[self.currentCard])
				self.library[self.library.index(x)+self.chunkSize]["learned"] = False
				self.library.pop(self.currentCard)
				self.difficulty += 1
				break

	def addCard(self):
		self.library.append("{'answer': 'Die ADDADADAD', 'learned': False, 'question': 'newspaper', 'chunk': 0}")

	def refreshCurrentDeck(self):
		self.loadVocabs()
		for x in self.library:
			x["difficulty"] = 1 # hier kann man noch was machen
		self.saveVocabs()

################# UTILITY ##################

	def setChunks(self):
		i = 0
		n = 0
		for x in self.library:
			self.numberOfChunks = n+1
			x["chunk"] = n
			i += 1
			if i is self.chunkSize:
				n += 1
				i = 0

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadVocabs("deutsch")
	myLibrary.loadDecks()
