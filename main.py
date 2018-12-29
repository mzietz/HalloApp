#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
import json
import os
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
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
	picture = StringProperty("data/pictures/blackboard.png")
	text = StringProperty('Hier steht Deckname')

class HomePage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	text = StringProperty('Welcome')
	study_button_size = ListProperty([700,700]) #250
	data_button_size = ListProperty([400,400]) #170
	settings_button_size = ListProperty([400,400])

class ChunkPage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	text = StringProperty('저장했습니다!')

class SettingsPage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	listpicture = StringProperty("data/pictures/stickynote_weiss.png")
	text = StringProperty('Settings')

class DataPage(Screen):
	picture = StringProperty("data/pictures/blackboard.png")
	listpicture = StringProperty("data/pictures/stickynote_weiss.png")
	text = StringProperty('Data')
	a1_image = StringProperty("data/pictures/A1.png")
	a2_image = StringProperty("data/pictures/A2.png")
	b1_image = StringProperty("data/pictures/B1.png")
	b2_image = StringProperty("data/pictures/B2.png")

#class DeckData(RecycleView):
#	def __init__(self, **kwargs):
#		super(DeckData, self).__init__(**kwargs)
#		self.data = []
#		self.deck = ""
#		self.initialized = 0
#
#class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
# 								 RecycleBoxLayout):
# 	pass

# class SelectableLabel(RecycleDataViewBehavior, Label):
# 	index = 0
# 	selected = BooleanProperty(False)
# 	selectable = BooleanProperty(True)
	
# 	def prints(self):
# 		print "print"

# 	def refresh_view_attrs(self, rv, index, data):
# 		self.index = index
# 		for x in rv.data:
# 			if x["selected"] == True:
# 				rv.parent.parent.parent.parent.parent.text = x["text"]

# 		return super(SelectableLabel, self).refresh_view_attrs(
# 			rv, index, data)

# 	def on_touch_down(self, touch):
# 		if super(SelectableLabel, self).on_touch_down(touch):
# 			return True
# 		if self.collide_point(*touch.pos) and self.selectable:
# 			return self.parent.select_with_touch(self.index, touch)

# 	def apply_selection(self, rv, index, is_selected):
# #		print index
# 		for x in rv.data:
# 			x["selected"] = False
# 		if is_selected == True:
# #			rv.data[-1]["selected"] = False
# 			rv.data[index]["selected"] = True
# 			rv.parent.parent.parent.parent.parent.text = rv.data[index]["text"]
# #			print str(rv.data[index]["text"]) + "is selected"
# #			print str(rv.data[0]["text"]) + " " + str(rv.data[0]["selected"])
# #			print str(rv.data[1]["text"]) + " " + str(rv.data[1]["selected"])
# #			print str(rv.data[2]["text"]) + " " + str(rv.data[2]["selected"])
# #			print str(rv.data[3]["text"]) + " " + str(rv.data[3]["selected"])
# #			print str(rv.data[4]["text"]) + " " + str(rv.data[4]["selected"])
# #			print str(rv.data[5]["text"]) + " " + str(rv.data[5]["selected"])
# #		else:
# #			rv.data[index]["selected"] = False
	

class SwipeCardsApp(App):
	vocab1 = StringProperty()
	vocab2 = StringProperty()
	answer1 = StringProperty()
	answer2 = StringProperty()
	info11 = StringProperty()
	info12 = StringProperty()
	info21 = StringProperty()
	info22 = StringProperty()

	currentDeck = StringProperty()
	currentDeckInfo = StringProperty()

	cardsStudied = StringProperty()
	cardsNotStudied = StringProperty()
	
	def build(self):
		kivy.Config.set('graphics', 'width',  380)
		kivy.Config.set('graphics', 'height', 610)
		self.title = 'Swiper'
		self.sm = SwipeManager()
		self.sm.transition = SlideTransition(duration=.4, direction='left')
		self.homepage = HomePage(name = 'home')
		self.vocabfrontpage = VocabFrontPage(name = 'vocabfrontpage')
		self.settingspage = SettingsPage(name = 'settingspage')
		self.datapage = DataPage(name = 'datapage')
		self.chunkpage = ChunkPage(name = 'chunkpage')
		self.pageone = PageOne(name ='pageone')
		self.pagetwo = PageTwo(name ='pagetwo')
		self.sm.add_widget(self.homepage)
		self.sm.add_widget(self.settingspage)
		self.sm.add_widget(self.datapage)
		self.sm.add_widget(self.vocabfrontpage)
		self.sm.add_widget(self.chunkpage)
		self.sm.add_widget(self.pageone)
		self.sm.add_widget(self.pagetwo)
		self.sm.current = 'home'
		self.lib = Library()
		self.lib.loadDecks()
		self.set_current_deck()
		print "Initialisiert mit: " +str(self.currentDeck + " und " + str(self.lib.currentDeck))
		return self.sm

	def init(self):
#		print "init"
		self.lib.resetLearnedStatus()
		self.lib.currentChunk = self.lib.nextChunk()
		self.lib.nextCard()
		self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
		self.answer1 = ""
		self.info11 = ""
		self.info12 = ""
		self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
		self.answer2 = ""
		self.info21 = ""
		self.info22 = ""
		self.answered = False
		self.cardsStudied = str(self.lib.cardsStudied())
		self.cardsNotStudied = str(self.lib.cardsNotStudied())
		self.lib.difficulty = 0

	def go_to_vocabfrontpage(self):
		self.sm.transition.direction = 'left'
		self.sm.current = 'vocabfrontpage'

	def set_current_deck(self):
		for x in self.lib.decks:
			if x["selected"] == True:
				self.currentDeck = x["text"][2:]
				self.currentLevel = x["text"][:2]
				self.lib.currentDeck = x["text"]

		# reset images
		self.datapage.a1_image = "data/pictures/A1.png"
		self.datapage.a2_image = "data/pictures/A2.png"
		self.datapage.b1_image = "data/pictures/B1.png"
		self.datapage.b2_image = "data/pictures/B2.png"
		if self.currentLevel == "a1":
			self.datapage.a1_image = "data/pictures/A1groß.png"
		if self.currentLevel == "a2":
			self.datapage.a2_image = "data/pictures/A2groß.png"		
		if self.currentLevel == "b1":
			self.datapage.b1_image = "data/pictures/B1groß.png"		
		if self.currentLevel == "b2":
			self.datapage.b2_image = "data/pictures/B2groß.png"
		self.lib.saveDecks()

		print "Current Level is: " + str(self.currentLevel)
		print "Current Deck is: " + str(self.currentDeck)

	def go_to_settings(self):
#		self.homepage.settings_button_size = [170,170]
		self.sm.transition.direction = 'right'
		self.sm.current = 'settingspage'	

	def go_to_data(self):
#		self.homepage.data_button_size = [170,170]
		self.set_current_deck()
		self.sm.transition.direction = 'right'
		self.sm.current = 'datapage'

	def go_to_vocab(self):
		self.sm.transition.direction = 'left'
		self.lib.loadVocabs()
		self.init()
		self.sm.current = 'pageone'

	def go_to_chunkpage(self):
		self.sm.transition.direction = 'left'
		self.cardsStudied = str(self.lib.cardsStudied())
		self.cardsNotStudied = str(self.lib.cardsNotStudied())
		self.sm.current = 'chunkpage'

	def go_to_home(self):
		self.sm.transition.direction = 'left'
		self.sm.current = 'home'

	def go_to_one(self, direction):
		self.answered = False
		if self.lib.cardsLeft() == 1 and direction == 'left':
			self.lib.saveVocabs()
			self.go_to_chunkpage()
		else:	
			if direction == 'left':
				self.lib.iknowCard()
			elif direction == 'right':
				self.lib.idontknowCard()
			self.lib.nextCard()
			self.vocab1 = self.lib.library[self.lib.currentCard]["question"]
			self.answer1 = ""
			self.info11 = ""
			self.info12 = ""
			self.sm.transition.direction = direction
#			self.debug()
			self.sm.current = 'pageone'

	def go_to_two(self, direction):
		self.answered = False
		if self.lib.cardsLeft() == 1 and direction == 'left':
			self.lib.saveVocabs()
			self.go_to_chunkpage()
		else:
			if direction == 'left':
				self.lib.iknowCard()
			elif direction == 'right':
				self.lib.idontknowCard()
			self.lib.nextCard()
			self.vocab2 = self.lib.library[self.lib.currentCard]["question"]
			self.answer2 = ""
			self.info21 = ""
			self.info22 = ""
			self.sm.transition.direction = direction
#			print self.lib.currentCard
#			self.debug()
			self.sm.current = 'pagetwo'
	
	def show_answer(self, screen):
		if screen == self.pageone:
			self.answer1 = self.lib.library[self.lib.currentCard]["answer"]
			self.info11 = self.lib.library[self.lib.currentCard]["info1"]
			self.info12 = self.lib.library[self.lib.currentCard]["info2"]
		elif screen == self.pagetwo:
			self.answer2 = self.lib.library[self.lib.currentCard]["answer"]
			self.info21 = self.lib.library[self.lib.currentCard]["info1"]
			self.info22 = self.lib.library[self.lib.currentCard]["info2"]
	
	def debug(self):
		for i,x in enumerate(self.lib.library):
			print str(i) + x["question"] 

	def touchdown(self, touch):
		self.coordinate = touch.x	

	def resetCurrentDeck(self):
		self.lib.refreshCurrentDeck()
		print "refresh" + str(self.currentDeck)

	def touchup_on_pagetwo(self, touch):
		try:
			self.distance = touch.x - self.coordinate		
		except:
			print "Zu schnell"
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
		try:
			self.distance = touch.x - self.coordinate	
		except:
			print "zu schnell"
		if self.distance < -50:
			self.go_to_vocab()	

	def touchup_on_chunkpage(self, touch):
		self.distance = touch.x - self.coordinate		
		if self.distance < -50:
			self.go_to_vocab()	

	def on_level_button(self, level):
		self.datapage.a1_image = "data/pictures/A1.png"
		self.datapage.a2_image = "data/pictures/A2.png"
		self.datapage.b1_image = "data/pictures/B1.png"
		self.datapage.b2_image = "data/pictures/B2.png"
		if level == "A1":
			self.currentLevel = "a1"
			self.datapage.a1_image = "data/pictures/A1groß.png"
		if level == "A2":
			self.currentLevel = "a2"
			self.datapage.a2_image = "data/pictures/A2groß.png"		
		if level == "B1":
			self.currentLevel = "b1"
			self.datapage.b1_image = "data/pictures/B1groß.png"		
		if level == "B2":
			self.currentLevel = "b2"
			self.datapage.b2_image = "data/pictures/B2groß.png"
	
	def on_deck_button(self, deck):
		self.currentDeck = self.currentLevel + deck
		self.lib.currentDeck = self.currentDeck
		self.lib.saveDecks()	
		print "Current Level is: " + str(self.currentLevel)
		print "Current Deck is: " + str(self.currentDeck)

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