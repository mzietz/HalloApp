#!/usr/bin/env python

from os.path import join, exists
from operator import itemgetter, attrgetter
from collections import Counter
from random import shuffle
import json
import datetime
import random
import math

class Library:
    def __init__(self):
        self.current_card = 0
        self.current_chunk = 0
        self.current_deck = ""
        self.difficulty = 1
        self.chunk_size = 10
        self.date = datetime.datetime.now()
        self.firsttime = None
        self.finished = False
        
    def __repr__(self):
        return "Library({})".format(self.date)

    def load_decks(self):
        with open(join("data/", 'decks.json')) as fd:
            data = json.load(fd)
            self.decks = data["decks"]
            self.firsttime = data["firsttime"]

    def save_decks(self):
        for x in self.decks:
            if x["text"] == self.current_deck:
                x["selected"] = True
            else:
                x["selected"] = False
        with open(join("data/", 'decks.json'), 'w') as fd:
            data = { "firsttime" : self.firsttime, "decks" : self.decks}
            json.dump(data, fd, indent=2)
    
    def load_vocabs(self):
        with open(join("data/", self.current_deck+'.json')) as fd:
            self.library = json.load(fd)
    
    def reset_learned_status(self):
        for x in self.library:
            x["learned"] = False

    def save_vocabs(self):
        for x in self.library:
            if x["chunk"] == self.current_chunk:
                x["difficulty"] = self.difficulty
                x["date"] = unicode(datetime.datetime.now())
        
        with open(join("data/", self.current_deck+'.json'), 'w') as fd:
            json.dump(self.library, fd, indent=2)

            
    def next_card(self):
        for x in self.library:
            if x["learned"] == False and x["chunk"] == self.current_chunk:
                self.current_card = self.library.index(x)
                # print "index" +str(self.library.index(x))
                break
        
    def cards_left(self):
        i=0
        for x in self.library:
            if x["learned"] == False and x["chunk"] == self.current_chunk:
                i+=1    
        return i

    def cards_studied(self):
        i=0
        for x in xrange(int(math.ceil(len(self.library)/self.chunk_size))):
            if self.library[x*self.chunk_size]["difficulty"] == 0:
                i+=1    
        return i

    def cards_not_studied(self):
        i=0
        for x in xrange(int(math.ceil(len(self.library)/float(self.chunk_size)))):
            if self.library[x*self.chunk_size]["difficulty"] != False:
                i+=1    
        return i
    
    def next_chunk(self):
        self.nextThree = []
        self.finished = False
        for x in xrange(3):
            if len(self.library) > 30: # in case of not yet implemented decks get selected
                s = sorted(self.library, key=lambda k: (k['difficulty'], k['date']), reverse=True)[x*self.chunk_size]
            else:
                return 0
            if s['difficulty'] != 0:
                self.nextThree.append(s["chunk"])
        self.difficulty = 0
        if not self.nextThree:
            self.finished = True
            return 0
        else:
            return random.choice(self.nextThree)
    
    def i_know_card(self):
        self.library[self.current_card]["learned"] = True

    def i_dont_know_card(self):
        for x in self.library:
            if x["chunk"] is self.current_chunk:
                if self.get_chunksize() == self.chunk_size:
                    self.library.insert(self.library.index(x)+self.get_chunksize(),self.library[self.current_card])
                    self.library[self.library.index(x)+self.get_chunksize()]["learned"] = False
                else:
                    self.library.append(self.library[self.current_card])
                    self.library[-1]["learned"] = False
                self.library.pop(self.current_card)
                self.difficulty += 1
                break

    def reset_deck(self):
        self.load_vocabs()
        self.shuffle_library()
 #       print self.library[0]["question"]
        for x in self.library:
            x["difficulty"] = 1
            x["date"] = unicode(datetime.datetime.now())
        # shuffle(self.library)
#        with open(join("data/", 'cache.json'), 'w') as fd:
        with open(join("data/", self.current_deck+'.json'), 'w') as fd:
            json.dump(self.library, fd, indent=2)

    def shuffle_library(self):
        shuffle(self.library)
        i=0
        n=0
        for x in self.library:
            x["chunk"] = i
            n+=1
            if n == self.chunk_size:
                i+=1
                n=0

    def get_chunksize(self):
        c = Counter(x["chunk"] for x in self.library)
        return c[self.current_chunk]

if __name__=="__main__":
    myLibrary = Library()
    myLibrary.load_decks()
    myLibrary.current_deck = "a1adjektive"
    myLibrary.load_vocabs()
    myLibrary.reset_deck()
#   myLibrary.cardsNotStudied()
#   print len(myLibrary.library)
#   myLibrary.firsttime = True
#   print myLibrary.firsttime
#   myLibrary.save_decks()
