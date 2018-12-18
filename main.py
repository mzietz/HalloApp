#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
import json
import os
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty, NumericProperty
from operator import itemgetter, attrgetter
from jsonlibrary import *


class SwipeManager(ScreenManager):
	pass

class PageOne(Screen):
	pass

class PageTwo(Screen):
	pass

class VocabFrontPage(Screen):
	picture = StringProperty("data/pictures/app_welcome.png")
	text = StringProperty('공부하는 방법')

class HomePage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	text = StringProperty('Welcome')
	study_button_size = ListProperty([250,250])
	data_button_size = ListProperty([170,170])
	settings_button_size = ListProperty([170,170])

class ChunkPage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	text = StringProperty('Progress Saved')

class SettingsPage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	listpicture = StringProperty("data/pictures/stickynote_weiss.png")
	text = StringProperty('Settings')

class DataPage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	listpicture = StringProperty("data/pictures/stickynote_weiss.png")
	text = StringProperty('Data')

class SwipeCardsApp(App):
	vocab1 = StringProperty()
	vocab2 = StringProperty()
	answer1 = StringProperty()
	answer2 = StringProperty()
	
	def build(self):
		kivy.Config.set('graphics', 'width',  380)
		kivy.Config.set('graphics', 'height', 610)
		self.title = 'Swiper'
		self.sm = SwipeManager()
		self.sm.transition = SlideTransition(duration=.4, direction='left')
		self.homepage = HomePage(name = 'home')
		self.vocabfrontpage = VocabFrontPage(name = 'vocabfrontpage')
		self.settings = SettingsPage(name = 'settings')
		self.datapage = DataPage(name = 'datapage')
		self.chunkpage = ChunkPage(name = 'chunkpage')
		self.pageone = PageOne(name ='pageone')
		self.pagetwo = PageTwo(name ='pagetwo')
		self.sm.add_widget(self.homepage)
		self.sm.add_widget(self.settings)
		self.sm.add_widget(self.datapage)
		self.sm.add_widget(self.vocabfrontpage)
		self.sm.add_widget(self.chunkpage)
		self.sm.add_widget(self.pageone)
		self.sm.add_widget(self.pagetwo)
		self.sm.current = 'home'
#		self.init()
		return self.sm

	def init(self):
#		print "init"
		self.lib = Library()
		self.lib.loadVocabs("Deutsch")
		self.lib.loadProgress()
		self.lib.chunkSize = 4
		self.lib.setChunks()
		self.lib.currentChunk = self.lib.nextChunk()
		self.lib.nextCard()
		self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
		self.answer1 = ""
		self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
		self.answer2 = ""
		self.answered = False
		self.lib.difficulty = 0

	def go_to_vocabfrontpage(self):
		self.homepage.study_button_size = [170,170]
		self.sm.transition.direction = 'left'
		self.sm.current = 'vocabfrontpage'

	def go_to_settings(self):
		self.homepage.settings_button_size = [170,170]
		self.sm.transition.direction = 'right'
		self.sm.current = 'settings'	

	def go_to_data(self):
		self.homepage.data_button_size = [170,170]
		self.sm.transition.direction = 'right'
		self.sm.current = 'datapage'

	def go_to_vocab(self):
		self.sm.transition.direction = 'left'
		self.init()
		self.sm.current = 'pageone'

	def go_to_chunkpage(self):
		self.sm.transition.direction = 'left'
		self.sm.current = 'chunkpage'

	def go_to_one(self, direction):
		self.answered = False
		if self.lib.cardsLeft() == 1 and direction == 'left':
			self.lib.saveProgress()
			self.go_to_chunkpage()
		else:	
			if direction == 'left':
				self.lib.iknowCard()
			elif direction == 'right':
				self.lib.idontknowCard()
			self.lib.nextCard()
			self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
			self.answer1 = ""
			self.sm.transition.direction = direction
			self.sm.current = 'pageone'

	def go_to_two(self, direction):
		self.answered = False
		if self.lib.cardsLeft() == 1 and direction == 'left':
			self.lib.saveProgress()
			self.go_to_chunkpage()
		else:
			if direction == 'left':
				self.lib.iknowCard()
			elif direction == 'right':
				self.lib.idontknowCard()

			self.lib.nextCard()
			self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
			self.answer2 = ""
			self.sm.transition.direction = direction
			self.sm.current = 'pagetwo'
	
	def show_answer(self, screen):
		if screen == self.pageone:
			self.answer1 = self.lib.library[self.lib.currentCard]["answer"]
		elif screen == self.pagetwo:
			self.answer2 = self.lib.library[self.lib.currentCard]["answer"]
	
	def touchdown(self, touch):
		self.coordinate = touch.x

	def touchup_on_pagetwo(self, touch):
		self.distance = touch.x - self.coordinate		
		if self.answered == False:
			self.show_answer(self.pagetwo)
			self.answered = True
		else:
			if self.distance > 50:
				self.go_to_one('right')
			elif self.distance < -50:
				self.go_to_one('left')

	def touchup_on_pageone(self, touch):
		self.distance = touch.x - self.coordinate		
		if self.answered == False:
			self.show_answer(self.pageone)
			self.answered = True
		else:
			if self.distance > 50:
				self.go_to_two('right')
			elif self.distance < -50:
				self.go_to_two('left')
	
	def touchup_on_vocabfrontpage(self, touch):
		self.distance = touch.x - self.coordinate		
		if self.distance < -50:
			self.go_to_vocab()

	def touchup_on_chunkpage(self, touch):
		self.distance = touch.x - self.coordinate		
		if self.distance < -50:
			self.go_to_vocab()	

	def pushedbutton(self):
		print self.homepage.ids.items()
		for key in self.homepage.ids.items():
			if key[0] == "study_button":
				self.homepage.study_button_size = [240,240]
			if key[0] == "data_button":
				self.homepage.data_button_size = [160,160]
			if key[0] == "setting_button":
				self.homepage.setting_button_size = [160,160]
if __name__ == '__main__':
	SwipeCardsApp().run()