#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

data = []

class Filer():
	def __init__(self):
		self.data = None
	def openJSON(self, name):
		with open(name) as fd:
			self.data = json.load(fd)

	def loadTXT(self, name):
		with open(name) as f:
			for line in f:
				print line

	def saveTXT(self, name):
		with open(name, 'w') as fd:
			for line in self.data:
				fd.write(line.encode('utf-8') + "\n")

if __name__ == '__main__':
	myFiler = Filer()
	myFiler.openTXT("A1Verben.json")
	myFiler.saveTXT("text.txt")
	print myFiler.data[1]
