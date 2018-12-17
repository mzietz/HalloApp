#!/usr/bin/env python

from os.path import join, exists
from operator import itemgetter, attrgetter
from random import shuffle
import json

class Library:
	def __init__(self):
		self.currentCard = 0
		self.currentChunk = 0
		self.difficulty = 0

	def loadJSON(self):
		with open(join("data/", 'Deutsch.json')) as fd:
			self.library = json.load(fd)

	def saveJSON(self):
		with open(join("data/", 'Save.json')) as fd:
			self.save = json.load(fd)
		for x in self.save:
			if x["chunk"] == self.currentChunk:
				x["difficulty"] = self.difficulty
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
		with open(join("data/", 'Save.json')) as fd:
			self.save = json.load(fd)
		self.difficulty = 0
		for x in self.save:
			if x["difficulty"] > self.difficulty:
				self.difficulty = x["difficulty"]
				self.currentChunk = x["chunk"]
		self.difficulty = 0
		return self.currentChunk

	def iknowCard(self):
		self.library[self.currentCard]["learned"] = True

	def idontknowCard(self):
		self.library.append(self.library[self.currentCard])
		self.library[-1]["learned"] = False
		self.library.pop(self.currentCard)
		self.difficulty += 1

#	@property
#	def vocabulary_fn(self):
#		return join('Deutsch.json')

if __name__=="__main__":
	myLibrary = Library()
	myLibrary.loadJSON()
#	print(myLibrary.cardsLeft())
#	myLibrary.nextCard()
#	print(myLibrary.library)
	myLibrary.saveJSON()
	print myLibrary.nextChunk()
#	print myLibrary.save
#	print myLibrary.nextCard()
