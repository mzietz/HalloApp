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
		self.firsttime = None

	def loadDecks(self):
		with open(join("data/", 'decks.json')) as fd:
			data = json.load(fd)
			self.decks = data["decks"]
			self.firsttime = data["firsttime"]

	def saveDecks(self):
		for x in self.decks:
			if x["text"] == self.currentDeck:
				x["selected"] = True
			else:
				x["selected"] = False
		with open(join("data/", 'decks.json'), 'w') as fd:
			data = { "firsttime" : self.firsttime, "decks" : self.decks}
			json.dump(data, fd, indent=2)
	
	def loadVocabs(self):
		with open(join("data/", self.currentDeck+'.json')) as fd:
			self.library = json.load(fd)
	
	def resetLearnedStatus(self):
		for x in self.library:
			x["learned"] = False

	def saveVocabs(self):
		for x in self.library:
			if x["chunk"] == self.currentChunk:
				x["difficulty"] = self.difficulty
				x["date"] = unicode(datetime.datetime.now())
		
		with open(join("data/", self.currentDeck+'.json'), 'w') as fd:
			json.dump(self.library, fd, indent=2)

			
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
		for x in xrange(len(self.library)/self.chunkSize):
			if self.library[x*self.chunkSize]["difficulty"] == 0:
				i+=1	
		return i

	def cardsNotStudied(self):
		i=0
		for x in xrange(len(self.library)/self.chunkSize):
			if self.library[x*self.chunkSize]["difficulty"] != False:
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
		self.difficulty = 0 # wird gesetzt bei go_to_vocab()
		self.date = datetime.datetime.now()
#		print self.currentChunk
		return self.currentChunk

	def iknowCard(self):
		self.library[self.currentCard]["learned"] = True

	def idontknowCard(self):
		for x in self.library:
			if x["chunk"] is self.currentChunk:
				s = self.getRealChunksize()
				self.library.insert(self.library.index(x)+self.chunkSize,self.library[self.currentCard])
				try:
					self.library[self.library.index(x)+self.chunkSize]["learned"] = False
				except:
					self.library[self.library.index(x)+s]["learned"] = False
				self.library.pop(self.currentCard)
				self.difficulty += 1
				break

	def refreshCurrentDeck(self):
		for x in self.library:
			x["difficulty"] = 1
			x["date"] = unicode(datetime.datetime.now())
		
		with open(join("data/", self.currentDeck+'.json'), 'w') as fd:
			json.dump(self.library, fd, indent=2)

	def getRealChunksize(self):
		i=0
		for x in self.library:
			if x["chunk"] is self.currentChunk:
				i+=1
		return i

if __name__=="__main__":
	myLibrary = Library()
#	myLibrary.loadVocabs("deutsch")
	myLibrary.loadDecks()
	print myLibrary.decks
	print myLibrary.firsttime
	myLibrary.saveDecks()
