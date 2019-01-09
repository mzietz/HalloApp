#!/usr/bin/env python

from os.path import join, exists
from operator import itemgetter, attrgetter
from collections import Counter
import json
import datetime
import random
import math

class Library:
	def __init__(self):
		self.currentCard = 0
		self.currentChunk = 0
		self.currentDeck = ""
		self.difficulty = 1
		self.chunkSize = 10
		self.date = datetime.datetime.now()
		self.firsttime = None
		self.finished = False
		
	def __repr__(self):
		return "Library({})".format(self.date)

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
		for x in xrange(int(math.ceil(len(self.library)/self.chunkSize))):
			if self.library[x*self.chunkSize]["difficulty"] == 0:
				i+=1	
		return i

	def cardsNotStudied(self):
		i=0
		for x in xrange(int(math.ceil(len(self.library)/float(self.chunkSize)))):
			if self.library[x*self.chunkSize]["difficulty"] != False:
				i+=1	
		return i
	
	def nextChunk(self):
		self.nextThree = []
		self.finished = False
		for x in xrange(3):
			s = sorted(self.library, key=lambda k: (k['difficulty'], k['date']), reverse=True)[x*self.chunkSize]
			if s['difficulty'] != 0:
				self.nextThree.append(s["chunk"])
		self.difficulty = 0
		if not self.nextThree:
			self.finished = True
		else:
			return random.choice(self.nextThree)
	
	def iknowCard(self):
		self.library[self.currentCard]["learned"] = True

	def idontknowCard(self):
		for x in self.library:
			if x["chunk"] is self.currentChunk:
				if self.getChunksize() == self.chunkSize:
					self.library.insert(self.library.index(x)+self.getChunksize(),self.library[self.currentCard])
					self.library[self.library.index(x)+self.getChunksize()]["learned"] = False
				else:
					self.library.append(self.library[self.currentCard])
					self.library[-1]["learned"] = False
				self.library.pop(self.currentCard)
				self.difficulty += 1
				break

	def refreshCurrentDeck(self):
		for x in self.library:
			x["difficulty"] = 1
			x["date"] = unicode(datetime.datetime.now())
		with open(join("data/", self.currentDeck+'.json'), 'w') as fd:
			json.dump(self.library, fd, indent=2)

	def getChunksize(self):
		c = Counter(x["chunk"] for x in self.library)
		return c[self.currentChunk]

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadDecks()
	myLibrary.currentDeck = "a1adjektive"
	myLibrary.loadVocabs()
#	myLibrary.cardsNotStudied()
#	print len(myLibrary.library)
#	myLibrary.firsttime = True
#	print myLibrary.firsttime
#	myLibrary.saveDecks()
