#!/usr/bin/env python

import kivy
import json
from os.path import join, exists
from os import listdir
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.uix.carousel import Carousel
from kivy.properties import ListProperty, NumericProperty
from operator import itemgetter, attrgetter
from random import shuffle
from library import *


class Page(GridLayout):
    pass

class HomeScreen(Screen):
	pass
#class MenuButton(ListItemButton):
#	index = NumericProperty(0)

class DeckScreen(Screen):
	pass
class LearnScreen(Screen):
	pass

#	pass
class ManageScreen(Screen):
	pass

class FlashcardsApp(App):
#	data = ListProperty(["Item #{0}".format(i) for i in range(50)])
	data = [{'text': str(i), 'is_selected': False} for i in range(100)]
	vocab = StringProperty()
	lib = Library()
	def build(self):
		self.lib = Library()
		self.lib.loadLibrary()
		self.currentDeck = 0
		self.vocab = self.lib.deck[self.currentDeck].card[0].question
		self.title = 'Flashcards'
		kivy.Config.set('graphics', 'width',  380)
		kivy.Config.set('graphics', 'height', 630)
		self.transition = SlideTransition(duration=.001)
		self.transition.direction = 'left'
		self.sm = ScreenManager()
		self.sm.add_widget(HomeScreen(name='home'))
		self.sm.add_widget(DeckScreen(name='deck'))
		self.sm.add_widget(LearnScreen(name='learn'))
		self.sm.current = 'home'
		return self.sm

	def show_answer(self):
		self.lib.deck[self.currentDeck].sortDeck()
		self.lib.deck[self.currentDeck].shuffleDeck() 
		self.vocab = self.lib.deck[self.currentDeck].card[0].answer

	def go_to_deckscreen(self):
		self.transition.duration = 0.2
		self.transition.direction = 'right'
		self.root.current = 'deck'

	def go_to_learnscreen(self):
		self.transition.duration = 0.2
		self.transition.direction = 'right'
		self.root.current = 'learn'
		self.lib.deck[0].sortDeck()
		self.lib.deck[0].shuffleDeck() 


if __name__ == '__main__':
	FlashcardsApp().run()