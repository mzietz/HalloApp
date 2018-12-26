#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
from os.path import join, exists


class ImportWords:
	def __init__(self):
		self.library = []
		self.deck = []
		self.chunkSize = 10
		self.txt = "raw_data/A1A2Verben.txt"
#### A1A2Verben #####
	def loadWordsfromTxt(self):
		n = 0
		i = 0
#		with open(self.txt) as f:
		for x, line  in enumerate(range(30)):
#			line = line.split()
			self.deck.append({"info1": "","info2": "", "date": "", "chunk": 0, "question": "", "difficulty": 0, "answer": "", "learned": False})
			self.deck[-1]["info1"] = ""
			self.deck[-1]["info2"] = ""
			self.deck[-1]["date"] = unicode(datetime.datetime.now())
			self.deck[-1]["answer"] = "Antwort " +str(x)
			self.deck[-1]["question"] = "Frage " +str(x)
			self.deck[-1]["learned"] = False
			self.deck[-1]["difficulty"] = 1
			self.deck[-1]["chunk"] = n
			i += 1
			if i is self.chunkSize:
				n += 1
				i = 0
############## Goethe Nomen A1 ##################	
#
	# def loadWordsfromTxt(self):
	# 	n = 0
	# 	i = 0
	# 	with open(self.txt) as f:
	# 		for line in f:
	# 			line = line.split("#")
	# 			self.deck.append({"info1": "","info2": "", "date": "", "chunk": 0, "question": "", "difficulty": 0, "answer": "", "learned": False})
	# 			self.deck[-1]["info1"] = ""
	# 			self.deck[-1]["info2"] = ""
	# 			self.deck[-1]["date"] = unicode(datetime.datetime.now())
	# 			self.deck[-1]["answer"] = line[1].rstrip()
	# 			self.deck[-1]["question"] = line[0].rstrip()
	# 			self.deck[-1]["learned"] = False
	# 			self.deck[-1]["difficulty"] = 1 # hier kann man noch was machen
	# 			self.deck[-1]["chunk"] = n
	# 			i += 1
	# 			if i is self.chunkSize:
	# 				n += 1
	# 				i = 0

	# def loadWordsfromTxt(self):
	# 	n = 0
	# 	i = 0
	# 	with open(self.txt) as f:
	# 		for line in f:
	# 			line = line.split("#")
	# 			self.deck.append({"info1": "","info2": "", "date": "", "chunk": 0, "question": "", "difficulty": 0, "answer": "", "learned": False})
	# 			self.deck[-1]["info1"] = ""
	# 			self.deck[-1]["info2"] = ""
	# 			self.deck[-1]["date"] = unicode(datetime.datetime.now())
	# 			self.deck[-1]["answer"] = line[0].rstrip()
	# 			self.deck[-1]["question"] = line[1].rstrip()
	# 			self.deck[-1]["learned"] = False
	# 			self.deck[-1]["difficulty"] = 1 # hier kann man noch was machen
	# 			self.deck[-1]["chunk"] = n
	# 			i += 1
	# 			if i is self.chunkSize:
	# 				n += 1
	# 				i = 0
	
	def saveWordsfromTxt(self):
		with open(join("Debug Deck.json"), 'w') as fd:
			json.dump(self.deck, fd)
		print("saved")


if __name__ == '__main__':
	myWords = ImportWords()
	myWords.loadWordsfromTxt()
	myWords.saveWordsfromTxt()
