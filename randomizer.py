#!/usr/bin/env python
from os.path import join
from random import shuffle
import json

class Randomizer:

    def __init__(self):
        self.decks = ["a1nomen", "a1verben", "a1adjektive", "a1rest", "a2nomen", "a2verben", "a2adjektive", "a2rest",
        "b1nomen", "b1verben", "b1adjektive", "b1rest"]
        self.library = None
        self.chunk_size = 10

    def load_vocabs(self, file):
        """Loads the vocabs of the current deck from its json file"""
        with open(join("data/", file +'.json')) as fd:
            self.library = json.load(fd)

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

    def save_vocabs(self, deck):       
        with open(join("data/", deck+'.json'), 'w') as fd:
            json.dump(self.library, fd, indent=2)

    def shuffle_all_decks(self):
        for deck in self.decks:
            self.load_vocabs(deck)
            self.shuffle_library()
            self.save_vocabs(deck)
            print deck
            print len(self.library)

if __name__ == '__main__':
    myRandomizer = Randomizer()
    myRandomizer.shuffle_all_decks()