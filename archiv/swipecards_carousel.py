#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from jsonlibrary import *


class PageOne(FloatLayout):
	def __init__(self, **kwargs):
		super(PageOne, self).__init__(**kwargs)
		self.text = "1"
class PageTwo(FloatLayout):
	def __init__(self, **kwargs):
		super(PageTwo, self).__init__(**kwargs)
		self.text = "2"

class WelcomePage(FloatLayout):
	def __init__(self, **kwargs):
		super(WelcomePage, self).__init__(**kwargs)
		self.text = "test"

class SwipeCardsApp(App):
	vocab1 = StringProperty()
	vocab2 = StringProperty()
	answer1 = StringProperty()
	answer2 = StringProperty()
	def build(self):
#		root = WelcomePage()
		self.carousel = Carousel()
		self.carousel.scroll_timeout = 0
		self.welcomepage = WelcomePage()
		self.carousel.add_widget(self.welcomepage)
#		self.carousel.remove_widget(self.welcomepage)
		self.pageone = PageOne()
		self.pagetwo = PageTwo()
		self.carousel.add_widget(self.pageone)
		self.carousel.add_widget(self.pagetwo)
		self.carousel.loop = True

		self.lib = Library()
		self.lib.loadJSON()
		self.vocab1 = self.lib.library[0]["question"]
		self.vocab2 = self.lib.library[1]["question"]
		self.answer1 = self.lib.library[0]["answer"]
		self.answer2 = self.lib.library[1]["answer"]
		return self.carousel

	def swipe(self):
		if str(type(self.carousel.current_slide)) =="<class '__main__.WelcomePage'>":
			print("HEllo")

		if str(type(self.carousel.current_slide)) =="<class '__main__.PageOne'>":
			print("SlideOne")
			print(str(self.lib.currentCard))
			self.lib.iknowCard()
			self.lib.nextCard()
			self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
			self.answer2 = self.lib.library[self.lib.currentCard]["answer"]
		if str(type(self.carousel.current_slide)) =="<class '__main__.PageTwo'>":
			print("SlideTwo")
			print(str(self.lib.currentCard))

			self.lib.iknowCard()
			self.lib.nextCard()
			self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
			self.answer1 = self.lib.library[self.lib.currentCard]["answer"]

	def swipe_right(self):
#		self.clearWelcomePage()
#		if str(type(self.carousel.current_slide)) =="<class '__main__.PageOne'>":
#			print("SlideOne")
			self.lib.iknowCard()
			self.lib.nextCard()
			self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
			self.answer1 = self.lib.library[self.lib.currentCard]["answer"]
	def swipe_left(self):	
#		if str(type(self.carousel.current_slide)) =="<class '__main__.PageTwo'>":
#			print("SlideTwo")
			self.lib.iknowCard()
			self.lib.nextCard()
			self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
			self.answer2 = self.lib.library[self.lib.currentCard]["answer"]
	def touchdown(self, touch):
		self.coordinate = touch.x

	def touchup(self, touch):
		self.distance = touch.x - self.coordinate
		if self.distance > 100:
#			print("right swipe!")
			self.carousel.load_previous()
#			self.swipe_right()
		elif self.distance < -100:
#			print("left swipe!")
#			self.swipe_left()
			self.carousel.load_next(mode='next')

if __name__ == '__main__':
	SwipeCardsApp().run()