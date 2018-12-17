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
		self.difficulty = 0
		self.chunkSize = 4
		self.numberOfChunks = 0
		self.date = datetime.datetime.now()

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


	def loadVocabs(self):
		with open(join("data/", 'Deutsch.json')) as fd:
			self.library = json.load(fd)
	def saveVocabs(self):
		with open(join("data/", 'Deutsch.json'), 'w') as fd:
			json.dump(self.library, fd)

	def loadProgress(self):
		with open(join("data/", 'Save.json')) as fd:
			self.save = json.load(fd)

	def saveProgress(self):
		for x in range(self.numberOfChunks):
			if x > self.numberOfChunks - len(self.save):
				self.save.append({"date": unicode(self.date), "difficulty": 0, "chunk": x, "learned": True})
		for x in self.save:
			if x["chunk"] == self.currentChunk:
				x["difficulty"] = self.difficulty
				x["date"] = unicode(datetime.datetime.now())
		
		with open(join("data/", 'Save.json'), 'w') as fd:
			json.dump(self.save, fd)

			
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

	def nextChunk(self):
#		with open(join("data/", 'Save.json')) as fd:
#			self.save = json.load(fd)
		self.date = datetime.datetime.now()
		for x in self.save:
			if x["difficulty"] > self.difficulty:
				self.difficulty = x["difficulty"]
				self.currentChunk = x["chunk"]
			if x["difficulty"] == self.difficulty and datetime.datetime.strptime(x["date"], '%Y-%m-%d %X.%f') < self.date:
				self.date = datetime.datetime.strptime(x["date"], '%Y-%m-%d %X.%f')
				self.currentChunk = x["chunk"]
		self.difficulty = 0
		self.date = datetime.datetime.now()
		return self.currentChunk

	def iknowCard(self):
		self.library[self.currentCard]["learned"] = True

	def idontknowCard(self):
		self.library.append(self.library[self.currentCard])
		self.library[-1]["learned"] = False
		self.library.pop(self.currentCard)
		self.difficulty += 1
	def addCard(self):
		self.library.append("{'answer': 'Die ADDADADAD', 'learned': False, 'question': 'newspaper', 'chunk': 0}")
#		pass
#	@property
#	def vocabulary_fn(self):
#		return join('Deutsch.json')

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadVocabs()
	myLibrary.loadProgress()
	print myLibrary.nextChunk()
#	print(myLibrary.cardsLeft())
#	myLibrary.nextCard()
#	print(myLibrary.library)
	myLibrary.setChunks()
#	myLibrary.saveVocabs()
	myLibrary.saveProgress()
#	print myLibrary.numberOfChunks
#	myLibrary.setChunks()

