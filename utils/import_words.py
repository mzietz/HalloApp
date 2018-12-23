#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
from os.path import join, exists


class ImportWords:
	def __init__(self):
		self.library = []
		self.deck = []
		self.chunkSize = 6
		self.txt = "A1A2Verben.txt"

	def loadWordsfromTxt(self):
		n = 0
		i = 0
		with open(self.txt) as f:
			for line in f:
				line = line.split()
				self.deck.append({"info1": "","info2": "", "date": "", "chunk": 0, "question": "", "difficulty": 0, "answer": "", "learned": False})
				self.deck[-1]["info1"] = "Präsens: " + line[-3]
				self.deck[-1]["info2"] = "Partizip II: " + line[-2]
				self.deck[-1]["date"] = unicode(datetime.datetime.now())
				self.deck[-1]["answer"] = line[0]
				if len(line) == 6:
					self.deck[-1]["question"] = line[-5]+ " " + line[-4]
				elif len(line) == 7:
					self.deck[-1]["question"] = line[-6]+ " " + line[-5]+ " " + line[-4]
				else:
					self.deck[-1]["question"] = line[-4]
				self.deck[-1]["learned"] = False
				self.deck[-1]["difficulty"] = 2
				self.deck[-1]["chunk"] = n
				i += 1
				if i is self.chunkSize:
					n += 1
					i = 0
#			print(self.liste)

	def saveWordsfromTxt(self):
		with open(join('Deutsch 1.json'), 'w') as fd:
			json.dump(self.deck, fd)
		print("saved")


if __name__ == '__main__':
	myWords = ImportWords()
	myWords.loadWordsfromTxt()
	print myWords.deck[4]
	print myWords.deck[5]
	print len(myWords.deck)
	myWords.saveWordsfromTxt()
