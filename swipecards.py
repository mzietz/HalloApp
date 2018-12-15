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


class SwipeManager(ScreenManager):
	pass
class PageOne(Screen):
	pass
class PageTwo(Screen):
	pass
class WelcomePage(Screen):
	pass

class SwipeCardsApp(App):
	vocab1 = StringProperty()
	vocab2 = StringProperty()
	answer1 = StringProperty()
	answer2 = StringProperty()
	def build(self):
		kivy.Config.set('graphics', 'width',  380)
		kivy.Config.set('graphics', 'height', 630)
		self.title = 'Swiper'
		self.sm = SwipeManager()
		self.sm.transition = SlideTransition(duration=.2, direction='left')
		self.welcomepage = WelcomePage(name = 'welcome')
		self.pageone = PageOne(name ='pageone')
		self.pagetwo = PageTwo(name ='pagetwo')
		self.sm.add_widget(self.welcomepage)
		self.sm.add_widget(self.pageone)
		self.sm.add_widget(self.pagetwo)
		self.sm.current = 'welcome'
		self.lib = Library()
		self.lib.loadJSON()
		self.vocab1 = self.lib.library[0]["question"]
		self.vocab2 = self.lib.library[1]["question"]
		self.answer1 = self.lib.library[0]["answer"]
		self.answer2 = self.lib.library[1]["answer"]
		return self.sm

	def go_from_welcome(self):
		self.sm.transition.direction = 'left'
		self.sm.current = 'pageone'

	def go_to_one(self, direction):
		self.sm.transition.direction = direction
		self.sm.current = 'pageone'

	def go_to_two(self, direction):
		self.sm.transition.direction = direction
		self.sm.current = 'pagetwo'


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

	def touchdown(self, touch):
		self.coordinate = touch.x

	def touchup(self, touch):
		print(str(self.sm.current))
		self.distance = touch.x - self.coordinate
		if self.sm.current == "welcome":
			self.go_from_welcome()
			print("welcome")
	
		elif self.sm.current == "pageone":
			print("one")

			if self.distance > 50:
				print("right swipe!")
				self.go_to_two('right')
			elif self.distance < -50:
				print("left swipe!")
				self.go_to_two('left')

		elif self.sm.current == "pagetwo":			
			print("two")
			if self.distance > 50:
				print("right swipe!")
				self.go_to_one('right')
			elif self.distance < -50:
				print("left swipe!")
				self.go_to_one('left')

if __name__ == '__main__':
	SwipeCardsApp().run()