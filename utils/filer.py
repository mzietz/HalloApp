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
    def putminusone(self):
        for line in self.data:
            line["difficulty"] = -1

    def saveTXT(self, name):
        with open(name, 'w') as fd:
            for line in self.data:
                fd.write(line.encode('utf-8') + "\n")
    def saveJSON(self, name):
        with open(name, 'w') as fd:
            json.dump(self.data, fd, indent=2)

if __name__ == '__main__':
    myFiler = Filer()
    myFiler.openJSON("a1adjektive.json")
    myFiler.putminusone()
    myFiler.saveJSON("text.json")
    print myFiler.data[1]
