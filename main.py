#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
import json
import os
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.properties import ListProperty, NumericProperty
from operator import itemgetter, attrgetter
from jsonlibrary import Library
from kivy.base import EventLoop

class SwipeManager(ScreenManager):
    pass

class PageOne(Screen):
    picture = StringProperty("data/pictures/anleitung.png")
    picture_opacity = NumericProperty(1)
class PageTwo(Screen):
    pass

class FinishedPage(Screen):
    picture = StringProperty("data/pictures/blackboard.png")

class VocabFrontPage(Screen):
    picture = StringProperty("data/pictures/blackboard.png")
    deck_image = StringProperty("")
    level_image = StringProperty("")

class HomePage(Screen):
    picture = StringProperty("data/pictures/blackboard.png")

class ChunkPage(Screen):
    picture = StringProperty("data/pictures/blackboard.png")

class AboutPage(Screen):
    picture = StringProperty("data/pictures/aboutpage.png")

class SettingsPage(Screen):
    picture = StringProperty("data/pictures/blackboard.png")
    deck_image = StringProperty("")
    level_image = StringProperty("")
    reset_string = StringProperty("재설정하기")
    listpicture = StringProperty("data/pictures/stickynote_weiss.png")

class DataPage(Screen):
    picture = StringProperty("data/pictures/blackboard.png")
    listpicture = StringProperty("data/pictures/stickynote_weiss.png")

    a1_image = StringProperty("data/pictures/A1.png")
    a2_image = StringProperty("data/pictures/A2.png")
    b1_image = StringProperty("data/pictures/B1.png")
    b2_image = StringProperty("data/pictures/B2.png")

    nomen_image = StringProperty("data/pictures/deck_pilz.png")
    verben_image = StringProperty("data/pictures/deck_pilz.png")
    adjektive_image = StringProperty("data/pictures/deck_pilz.png")
    rest_image = StringProperty("data/pictures/deck_pilz.png")  

class SwipeCardsApp(App):
    vocab1 = StringProperty()
    vocab2 = StringProperty()
    answer1 = StringProperty()
    answer2 = StringProperty()
    info11 = StringProperty()
    info12 = StringProperty()
    info21 = StringProperty()
    info22 = StringProperty()

    current_deck = StringProperty()
    currentDeckInfo = StringProperty()

    cards_studied = StringProperty()
    cards_not_studied = StringProperty()
    
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
        self.aboutpage = AboutPage(name ='aboutpage')
        self.finishedpage = FinishedPage(name ='finishedpage')
        self.sm.add_widget(self.homepage)
        self.sm.add_widget(self.aboutpage)
        self.sm.add_widget(self.settingspage)
        self.sm.add_widget(self.datapage)
        self.sm.add_widget(self.vocabfrontpage)
        self.sm.add_widget(self.chunkpage)
        self.sm.add_widget(self.finishedpage)
        self.sm.add_widget(self.pageone)
        self.sm.add_widget(self.pagetwo)
        self.sm.current = 'home'
        self.lib = Library()
        self.lib.load_decks()
        self.set_current_deck()
        self.lib.load_vocabs()
        self.load_intro()
        return self.sm

    def init(self):
        self.lib.reset_learned_status()
        self.lib.current_chunk = self.lib.next_chunk()
        self.lib.next_card()
        # print "größe Library:"+str(len(self.lib.library))
        # print "Current Card:"+str(self.lib.current_card)
        self.vocab1 = self.lib.library[self.lib.current_card]["question"]
        self.answer1 = ""
        self.info11 = ""
        self.info12 = ""
        self.vocab2 = self.lib.library[self.lib.current_card]["question"]
        self.answer2 = ""
        self.info21 = ""
        self.info22 = ""
        self.answered = False
        self.cards_studied = str(self.lib.cards_studied())
        self.cards_not_studied = str(self.lib.cards_not_studied())

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.sm.transition.direction = 'left'
            self.go_to_home()
            return True 

    def go_to_vocabfrontpage(self):
        self.sm.transition.direction = 'left'
        self.lib.load_vocabs()
        self.init()
        self.sm.current = 'vocabfrontpage'
        
    def set_current_deck(self):
        for x in self.lib.decks:
            if x["selected"] == True:
                self.current_deck = x["text"]
                self.currentLevel = x["text"][:2]
                self.lib.current_deck = x["text"]
                self.reset_level_pictures()
                self.choose_level_pictures(x["text"][:2])
                self.choose_deck_pictures(x["text"][2:])
                self.set_deck_and_level_images("settingspage", x["text"][:2],x["text"][2:])
        self.lib.save_decks()

    def go_to_settings(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'settingspage'    
        self.settingspage.reset_string = "재설정하기"

    def go_to_data(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'datapage'

    def go_to_vocab(self):
        self.sm.transition.direction = 'left'
        self.lib.load_vocabs()
        self.init()
        if self.lib.finished:
            self.sm.current = 'finishedpage'
        else:
            self.sm.current = 'pageone'

    def go_to_chunkpage(self):
        self.sm.transition.direction = 'left'
        self.lib.save_vocabs()
        self.lib.save_decks()
        self.cards_studied = str(self.lib.cards_studied())
        self.cards_not_studied = str(self.lib.cards_not_studied())
        self.sm.current = 'chunkpage'

    def go_to_home(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'home'

    def go_to_about(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'aboutpage'

    def go_to_one(self, direction):
        self.answered = False
        if self.lib.cards_left() == 1 and direction == 'left':
            self.go_to_chunkpage()
        else:   
            if direction == 'left':
                self.lib.i_know_card()
            elif direction == 'right':
                self.lib.i_dont_know_card()
            self.lib.next_card()
            self.vocab1 = self.lib.library[self.lib.current_card]["question"]
            self.answer1 = ""
            self.info11 = ""
            self.info12 = ""
            self.sm.transition.direction = direction
            self.sm.current = 'pageone'

    def go_to_two(self, direction):
        self.answered = False
        if self.lib.cards_left() == 1 and direction == 'left':
            self.go_to_chunkpage()
        else:
            if direction == 'left':
                self.lib.i_know_card()
            elif direction == 'right':
                self.lib.i_dont_know_card()
            self.lib.next_card()
            self.vocab2 = self.lib.library[self.lib.current_card]["question"]
            self.answer2 = ""
            self.info21 = ""
            self.info22 = ""
            self.sm.transition.direction = direction
            self.sm.current = 'pagetwo'
    
    def load_intro(self):
        if self.lib.firsttime:
            self.pageone.picture_opacity = 1
        else:
            self.pageone.picture_opacity = 0
        self.lib.firsttime = False
        self.lib.save_decks()

    def show_answer(self, screen):
        if screen == self.pageone:
            self.answer1 = self.lib.library[self.lib.current_card]["answer"]
            self.info11 = self.lib.library[self.lib.current_card]["info1"]
            self.info12 = self.lib.library[self.lib.current_card]["info2"]
        elif screen == self.pagetwo:
            self.answer2 = self.lib.library[self.lib.current_card]["answer"]
            self.info21 = self.lib.library[self.lib.current_card]["info1"]
            self.info22 = self.lib.library[self.lib.current_card]["info2"]
    
    def debug(self):
        for i,x in enumerate(self.lib.library):
            print str(i) + x["question"] 

    def touchdown(self, touch):
        self.coordinate = touch.x   

    def reset_current_deck(self):
        print self.current_deck
        self.lib.reset_deck()
        self.cards_studied = str(self.lib.cards_studied())
        self.cards_not_studied = str(self.lib.cards_not_studied())
        self.settingspage.reset_string = "재설정"

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
        try:
            self.distance = touch.x - self.coordinate
        except:
            pass
        if self.pageone.picture_opacity != 0:
            self.pageone.picture_opacity = 0    
        else:
            if self.answered == False:
                self.show_answer(self.pageone)
                self.answered = True
            else:
                if self.distance > 50:
                    self.go_to_two('right')
                elif self.distance < -50:
                    self.go_to_two('left')  

    def touchup_on_chunkpage(self, touch):
        self.distance = touch.x - self.coordinate       
        if self.distance < -50:
            self.go_to_vocab()  

    def on_level_button(self, level):
        self.reset_level_pictures()
        self.choose_level_pictures(level)
    
    def reset_deck_pictures(self):
        self.datapage.nomen_image = "data/pictures/deck_pilz.png"
        self.datapage.verben_image = "data/pictures/deck_pilz.png"
        self.datapage.adjektive_image = "data/pictures/deck_pilz.png"
        self.datapage.rest_image = "data/pictures/deck_pilz.png"

    def reset_level_pictures(self):
        self.datapage.a1_image = "data/pictures/A1.png"
        self.datapage.a2_image = "data/pictures/A2.png"
        self.datapage.b1_image = "data/pictures/B1.png"
        self.datapage.b2_image = "data/pictures/B2.png"
    
    def choose_deck_pictures(self, deck):
        if deck == "nomen":
            self.datapage.nomen_image = "data/pictures/nomen.png"
        if deck == "verben":
            self.datapage.verben_image = "data/pictures/verben.png"     
        if deck == "adjektive":
            self.datapage.adjektive_image = "data/pictures/adjektive.png"       
        if deck == "rest":
            self.datapage.rest_image = "data/pictures/rest.png"

    def choose_level_pictures(self, level):
        if level == "a1":
            self.currentLevel = "a1"
            self.datapage.a1_image = "data/pictures/A1gross.png"
            self.reset_deck_pictures()
        if level == "a2":
            self.currentLevel = "a2"
            self.datapage.a2_image = "data/pictures/A2gross.png"    
            self.reset_deck_pictures()    
        if level == "b1":
            self.currentLevel = "b1"
            self.datapage.b1_image = "data/pictures/B1gross.png"    
            self.reset_deck_pictures()    
        if level == "b2":
            self.currentLevel = "b2"
            self.datapage.b2_image = "data/pictures/B2gross.png"
            self.reset_deck_pictures()
    
    def on_deck_button(self, deck):
        self.current_deck = self.currentLevel + deck
        self.lib.current_deck = self.current_deck
        self.lib.save_decks()
        self.set_current_deck()
        self.reset_deck_pictures()
        self.choose_deck_pictures(deck)
        print self.lib.current_deck

    def set_deck_and_level_images(self, page, level, deck):
        if deck == "nomen":
            self.settingspage.deck_image = "data/pictures/nomen.png"
            self.vocabfrontpage.deck_image = "data/pictures/nomen.png"
        if deck == "verben":
            self.settingspage.deck_image = "data/pictures/verben.png"       
            self.vocabfrontpage.deck_image = "data/pictures/verben.png"     
        if deck == "adjektive":
            self.settingspage.deck_image = "data/pictures/adjektive.png"        
            self.vocabfrontpage.deck_image = "data/pictures/adjektive.png"      
        if deck == "rest":
            self.settingspage.deck_image = "data/pictures/rest.png"
            self.vocabfrontpage.deck_image = "data/pictures/rest.png"
        if level == "a1":
            self.settingspage.level_image = "data/pictures/A1.png"
            self.vocabfrontpage.level_image = "data/pictures/A1.png"
        if level == "a2":
            self.settingspage.level_image = "data/pictures/A2.png"  
            self.vocabfrontpage.level_image = "data/pictures/A2.png"    
        if level == "b1":
            self.settingspage.level_image = "data/pictures/B1.png"  
            self.vocabfrontpage.level_image = "data/pictures/B1.png"    
        if level == "b2":
            self.settingspage.level_image = "data/pictures/B2.png"
            self.vocabfrontpage.level_image = "data/pictures/B2.png"

if __name__ == '__main__':
    SwipeCardsApp().run()