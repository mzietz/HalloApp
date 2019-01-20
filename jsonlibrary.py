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
    """This class implements a flashcard deck."""
    def __init__(self):
        self.current_card = 0
        self.current_chunk = 0
        self.current_deck = ""
        self.difficulty = 1
        self.chunk_size = 10
        self.firsttime = None
        self.finished = False
        
    def __repr__(self):
        return "Library({})".format(self.date)

    def library_logger(orig_func):
        """Logging decorator logs all relevant library data"""
        import logging
        logging.basicConfig(level=logging.INFO)
        def wrapper(self):
            logging.info('Logger: Function: {}, Card: {}, Deck: {}, Chunk: {}, Difficulty: {}'.format(orig_func.__name__, self.current_card, self.current_deck, self.current_chunk, self.difficulty))
            return orig_func(self)
        return wrapper

    def load_decks(self):
        """Loads the decks from its json file"""
        with open(join("data/", 'decks.json')) as fd:
            data = json.load(fd)
            self.decks = data["decks"]
            self.firsttime = data["firsttime"]

    def save_decks(self):
        """Saves libraries decks to a json file"""
        for x in self.decks:
            if x["text"] == self.current_deck:
                x["selected"] = True
#                print "saved {} as current deck".format(self.current_deck)
            else:
                x["selected"] = False

        with open(join("data/", 'decks.json'), 'w') as fd:
            data = { "firsttime" : self.firsttime, "decks" : self.decks}
            json.dump(data, fd, indent=2)
    
    def load_vocabs(self):
        """Loads the vocabs of the current deck from its json file"""
        with open(join("data/", self.current_deck+'.json')) as fd:
            self.library = json.load(fd)
    
    def reset_learned_status(self):
        """Resets the status of all cards to not studied"""
        for x in self.library:
            if x["chunk"] == self.current_chunk:
                x["learned"] = False

    def save_vocabs(self):
        """Saves the vocabs of the current deck to its json file"""
        for x in self.library:
            if x["chunk"] == self.current_chunk:
                x["difficulty"] = self.difficulty
#                x["date"] = unicode(datetime.datetime.now())
        
        with open(join("data/", self.current_deck+'.json'), 'w') as fd:
            json.dump(self.library, fd, indent=2)
            
    def next_card(self):
        """Calculates which card appears next"""
        for x in self.library:
            if x["learned"] == False and x["chunk"] == self.current_chunk:
                self.current_card = self.library.index(x)
                break
        
    def cards_left(self):
        """Counts the decks left in the current chunk"""
        i=0
        for x in self.library:
            if x["learned"] == False and x["chunk"] == self.current_chunk:
                i+=1    
        return i

    def add_swipe(self, direction):
        """Adds left or right swipe to its respective counter"""
        if direction == 'right':
            for x in self.decks:
                if x["text"] == self.current_deck:
                    x["swipe_right"] += 1
#                    print "added right, total:" + str(x["swipe_right"])
        elif direction == 'left':
            for x in self.decks:
                if x["text"] == self.current_deck:
                    x["swipe_left"] += 1
#                    print "added left, total:" + str(x["swipe_left"])

    def next_chunk(self):
        """Calculats which chunk of cards is next"""
        self.nextThree = []
        self.finished = False
        for x in xrange(3):
            if len(self.library) > 30: # in case of not yet implemented decks get selected
                s = sorted(self.library, key=lambda k: k['difficulty'], reverse=True)[x*self.chunk_size]
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

    def swipe_value(self):
        for x in self.decks:
            if x["text"] == self.current_deck:
                return (x["swipe_left"], x["swipe_right"])

    @library_logger
    def i_know_card(self):
        """Sets learned status of current card to True"""
        self.library[self.current_card]["learned"] = True
        self.add_swipe('right')

    @library_logger
    def i_dont_know_card(self):
        """ Sets learned status of current card to False and outs card to the back of the current chunk"""
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
                self.add_swipe('left')
                break

    def reset_deck(self):
        """Resets and shuffles the current deck"""
        self.load_vocabs()
        self.shuffle_library()
        for x in self.library:
            x["difficulty"] = 1
            x["learned"] = False
        for x in self.decks:
            if x["text"] == self.current_deck:
                x["swipe_left"] = 0
                x["swipe_right"] = 0
        with open(join("data/", self.current_deck+'.json'), 'w') as fd:
            json.dump(self.library, fd, indent=2)

    def shuffle_library(self):
        """Shuffles the current deck"""
        shuffle(self.library)
        i=0
        n=0
        for x in self.library:
            x["chunk"] = i
            n+=1
            if n == self.chunk_size:
                i+=1
                n=0
        list(reversed(self.library))

    def get_chunksize(self):
        """Calculates the amount of cards in a chunk"""
        c = Counter(x["chunk"] for x in self.library)
        return c[self.current_chunk]

if __name__=="__main__":
    myLibrary = Library()
    myLibrary.load_decks()
    myLibrary.current_deck = "a1adjektive"
    myLibrary.load_vocabs()
