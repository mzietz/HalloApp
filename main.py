#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
import json
import os
import random
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import FocusBehavior
from operator import itemgetter, attrgetter
from jsonlibrary import Library
from kivy.base import EventLoop

from kivy.animation import Animation
from kivy.clock import Clock

class SwipeManager(ScreenManager):
    pass

class PageOne(Screen):
    picture = StringProperty("data/pictures/anleitung.png")
    picture_answer = StringProperty("")
    picture_opacity = NumericProperty(1)
    line_image = StringProperty("")

    def __init__(self, **kwargs):
        super(PageOne, self).__init__(**kwargs)
        self.ids.right.pos_hint ={'center_y': -0.3, 'center_x': .5}
        self.ids.right.size_hint =(0.7, 1)

    def on_pre_enter(self):
        animation = Animation(pos_hint = {'center_y': 0.2}, t='in_out_cubic', duration=0.5)
        animation += Animation(pos_hint = {'center_y': -0.3}, t='in_out_cubic', duration=0.7)
        animation.start(self.ids.right)

class PageTwo(Screen):
    picture_answer = StringProperty("")
    line_image = StringProperty("")

    def __init__(self, **kwargs):
        super(PageTwo, self).__init__(**kwargs)
        self.ids.right.pos_hint ={'center_y': -0.3, 'center_x': .5}
        self.ids.right.size_hint =(0.7, 1)

    def on_pre_enter(self):
        animation = Animation(pos_hint = {'center_y': 0.2}, t='in_out_cubic', duration=0.5)
        animation += Animation(pos_hint = {'center_y': -0.3}, t='in_out_cubic', duration=0.7)
        animation.start(self.ids.right)

class FinishedPage(Screen):
    back_image = StringProperty("data/pictures/mario_hand_schatten.png")
    picture = StringProperty("data/pictures/homescreen2.png")
    refresh_image = StringProperty("data/pictures/deck_refresh.png")
    back_image = StringProperty("data/pictures/mario_hand_schatten.png")
    
    def __init__(self, **kwargs):
        super(FinishedPage, self).__init__(**kwargs)
        self.ids.complete.pos_hint ={'center_y': 1.35, 'center_x': .5}
        self.ids.complete.size_hint =(.60, .60)

    def on_enter(self):
        animation = Animation(duration=.5)
        animation = Animation(pos_hint = {'center_y': 0.85}, t='in_out_cubic', duration=1)
        animation.start(self.ids.complete)

class VocabFrontPage(Screen):
    back_image = StringProperty("data/pictures/mario_hand_schatten.png")
    picture = StringProperty("data/pictures/homescreen2.png")
    start_image = StringProperty("data/pictures/start_pixel.png")
    deck = StringProperty("")
    level = StringProperty("")

class HomePage(Screen):
    picture = StringProperty("data/pictures/homescreen.png")
    data_image = StringProperty("data/pictures/data_button_stark.png")
    deck_image = StringProperty("data/pictures/deck_hallo.png")

class ChunkPage(Screen):
    picture = StringProperty("data/pictures/homescreen2.png")
    back_image = StringProperty("data/pictures/mario_hand_schatten.png")
    continue_image = StringProperty("data/pictures/weiter_pixel.png")
    deck = StringProperty("")
    level = StringProperty("")
    chunk_complete = BooleanProperty()
    def __init__(self, **kwargs):
        super(ChunkPage, self).__init__(**kwargs)
        self.ids.chunk_complete.pos_hint ={'center_y': 1.35, 'center_x': .5}
        self.ids.chunk_complete.size_hint =(.60, .60)

    def on_enter(self):
        if self.chunk_complete:
            animation = Animation(pos_hint = {'center_y': 0.85}, t='in_out_cubic', duration=0.5)
            animation.start(self.ids.chunk_complete)
        else:
            pass
    def reset_image(self):
        animation = Animation(pos_hint = {'center_y': 1.35}, t='in_out_cubic', duration=0.5)
        animation.start(self.ids.chunk_complete)
class AboutPage(Screen):
    picture = StringProperty("data/pictures/aboutdesign.png")
    back_image = StringProperty("data/pictures/mario_hand_schatten.png")

class DataPage(Screen):
    back_image = StringProperty("data/pictures/mario_hand_schatten.png")
    picture = StringProperty("data/pictures/homescreen2.png")
    size_image = StringProperty("data/pictures/weiter_pixel.png")
    a1_image = StringProperty("data/pictures/A1.png")
    a2_image = StringProperty("data/pictures/A2.png")
    b1_image = StringProperty("data/pictures/B1.png")
    # b2_image = StringProperty("data/pictures/B2.png")

    nomen_image = StringProperty("data/pictures/deck_hallo_raw.png")
    verben_image = StringProperty("data/pictures/deck_hallo_raw.png")
    adjektive_image = StringProperty("data/pictures/deck_hallo_raw.png")
    rest_image = StringProperty("data/pictures/deck_hallo_raw.png")
    deck_size = NumericProperty()
    deck_size_cache = NumericProperty()

    def __init__(self, **kwargs):
        super(DataPage, self).__init__(**kwargs)
        self.ids.size.pos_hint ={'center_y': -0.3, 'center_x': .7}
        self.ids.size.size_hint =(0.45, 0.45)

    def animate_deck_size(self, size):
        print size
        animation = Animation(pos_hint = {'center_y': -0.3}, t='in_out_cubic', duration=0.15)
        animation.bind(on_complete=self.deanimate_deck_size)
        self.deck_size_cache = size
        animation.start(self.ids.size)

    def deanimate_deck_size(self, *args):
        animation = Animation(pos_hint = {'center_y': 0.02}, t='in_out_cubic', duration=0.3)
        self.deck_size = self.deck_size_cache
        animation.start(self.ids.size)

    def animate_deck_size_out(self):
        animation = Animation(pos_hint = {'center_y': -0.3}, t='in_out_cubic', duration=0.15)
        animation.start(self.ids.size)

class HalloApp(App):
    vocab1 = StringProperty()
    vocab2 = StringProperty()
    answer1 = StringProperty()
    answer2 = StringProperty()
    info11 = StringProperty()
    info12 = StringProperty()
    info21 = StringProperty()
    info22 = StringProperty()
    current_deck = StringProperty()
    current_deck_size = NumericProperty()
    swipe_left_total = NumericProperty()
    swipe_right_total = NumericProperty()

    swipe_left_chunk = NumericProperty()
    swipe_right_chunk = NumericProperty()

    lines = ListProperty(["data/pictures/strich_alt_1.png", 
        "data/pictures/strich_alt_2.png", 
        "data/pictures/strich_alt_3.png", 
        "data/pictures/strich_alt_4.png",
        "data/pictures/strich_alt_5.png", 
        "data/pictures/strich_alt_6.png", 
        "data/pictures/strich_alt_7.png", 
        "data/pictures/strich_alt_8.png", 
        "data/pictures/strich_alt_9.png"])

    def build(self):
        kivy.Config.set('graphics', 'width',  380)
        kivy.Config.set('graphics', 'height', 610)
        self.title = 'Swiper'
        self.sm = SwipeManager()
        self.sm.transition = SlideTransition(duration=.4, direction='left')
        self.homepage = HomePage(name = 'home')
        self.vocabfrontpage = VocabFrontPage(name = 'vocabfrontpage')
        self.datapage = DataPage(name = 'datapage')
        self.chunkpage = ChunkPage(name = 'chunkpage')
        self.pageone = PageOne(name ='pageone')
        self.pagetwo = PageTwo(name ='pagetwo')
        self.aboutpage = AboutPage(name ='aboutpage')
        self.finishedpage = FinishedPage(name ='finishedpage')
        self.sm.add_widget(self.homepage)
        self.sm.add_widget(self.aboutpage)
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
        self.swipe_left_total, self.swipe_right_total = self.lib.swipe_value()
        return self.sm

    def init(self):
        self.lib.current_chunk = self.lib.next_chunk()
        self.lib.reset_learned_status()
        self.lib.next_card()
        self.vocab1 = self.lib.library[self.lib.current_card]["question"]
        self.answer1 = ""
        self.info11 = ""
        self.info12 = ""
        self.vocab2 = self.lib.library[self.lib.current_card]["question"]
        self.answer2 = ""
        self.info21 = ""
        self.info22 = ""
        self.answered = False
        # self.chunkpage.swipe_left, self.chunkpage.swipe_right = (self.lib.difficulty, 10)
        self.pageone.picture_answer = "data/pictures/empty.png"
        self.pagetwo.picture_answer = "data/pictures/empty.png"
        self.chunkpage.reset_image()

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
        self.set_random_line()
        self.swipe_left_total, self.swipe_right_total = self.lib.swipe_value()
        self.swipe_left_chunk, self.swipe_right_chunk = (0,0)
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

    def go_to_data(self):
        self.datapage.animate_deck_size_out()
        self.sm.transition.direction = 'left'
        self.set_current_deck()
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
        if self.lib.difficulty == 0:
            self.chunkpage.chunk_complete = True
        else:
            self.chunkpage.chunk_complete = False
        self.swipe_left_total, self.swipe_right_total = self.lib.swipe_value()
        self.swipe_left_chunk, self.swipe_right_chunk = (self.lib.difficulty, 10)
        self.sm.current = 'chunkpage'

    def go_to_home(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'home'

    def go_to_about(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'aboutpage'

    def go_to_one(self, direction):
        self.answered = False
        if self.lib.cards_left() == 1 and direction == 'left':
            self.lib.add_swipe('right')
            self.go_to_chunkpage()
        else:   
            if direction == 'left':
                self.lib.i_know_card()
                self.pageone.picture_answer = "data/pictures/plusone_green.png"
            elif direction == 'right':
                self.lib.i_dont_know_card()
                self.pageone.picture_answer = "data/pictures/plusone_red.png"
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
            self.lib.add_swipe('right')
            self.go_to_chunkpage()
        else:
            if direction == 'left':
                self.pagetwo.picture_answer = "data/pictures/plusone_green.png"
                self.lib.i_know_card()
            elif direction == 'right':
                self.pagetwo.picture_answer = "data/pictures/plusone_red.png"
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

    def touchdown(self, touch):
        self.coordinate = touch.x   

    def reset_current_deck(self):
        self.lib.reset_deck()

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

    def on_level_button(self, level):
        self.datapage.animate_deck_size_out()
        self.reset_level_pictures()
        self.choose_level_pictures(level)
    
    def reset_deck_pictures(self):
        self.datapage.nomen_image = "data/pictures/deck_hallo_raw.png"
        self.datapage.verben_image = "data/pictures/deck_hallo_raw.png"
        self.datapage.adjektive_image = "data/pictures/deck_hallo_raw.png"
        self.datapage.rest_image = "data/pictures/deck_hallo_raw.png"

    def reset_level_pictures(self):
        self.datapage.a1_image = "data/pictures/A1.png"
        self.datapage.a2_image = "data/pictures/A2.png"
        self.datapage.b1_image = "data/pictures/B1.png"
    
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
    
    def on_deck_button(self, deck):
        self.current_deck = self.currentLevel + deck
        self.lib.current_deck = self.current_deck
        self.lib.save_decks()
        self.set_current_deck()
        self.reset_deck_pictures()
        self.current_deck_size = self.lib.get_decksize()
        self.datapage.animate_deck_size(self.current_deck_size)
        self.choose_deck_pictures(deck)

    def button_animation(self):
        print "test"

    def set_deck_and_level_images(self, page, level, deck):
        if deck == "nomen":
            self.vocabfrontpage.deck = "명사"
            self.chunkpage.deck = "명사"
        if deck == "verben":
            self.vocabfrontpage.deck = "동사"     
            self.chunkpage.deck = "동사"
        if deck == "adjektive":
            self.vocabfrontpage.deck = "형용사"      
            self.chunkpage.deck = "형용사"
        if deck == "rest":
            self.vocabfrontpage.deck = "나머지"
            self.chunkpage.deck = "나머지"
        if level == "a1":
            self.vocabfrontpage.level = "A1"
            self.chunkpage.level = "A1"
        if level == "a2":
            self.vocabfrontpage.level = "A2"    
            self.chunkpage.level = "A2"    
        if level == "b1":
            self.vocabfrontpage.level = "B1"    
            self.chunkpage.level = "B1"    

    def click_animate(self, widget):
        if widget == "back":
            self.datapage.back_image = "data/pictures/mario_hand.png"
            self.vocabfrontpage.back_image = "data/pictures/mario_hand.png"
            self.chunkpage.back_image = "data/pictures/mario_hand.png"
            self.finishedpage.back_image = "data/pictures/mario_hand.png"
            self.aboutpage.back_image = "data/pictures/mario_hand.png"
        if widget == "data":
            self.homepage.data_image = "data/pictures/data_button_down.png"
        if widget == "vocab":
            self.homepage.deck_image = "data/pictures/deck_hallo_down.png"
        if widget == "continue":
            self.chunkpage.continue_image = "data/pictures/weiter_pixel_down.png"
        if widget == "start":
            self.vocabfrontpage.start_image = "data/pictures/start_pixel_down.png"
        if widget == "refresh":
            self.finishedpage.refresh_image = "data/pictures/deck_refresh_down.png"

    def reset_images(self, instance):
        self.vocabfrontpage.back_image = "data/pictures/mario_hand_schatten.png"
        self.datapage.back_image = "data/pictures/mario_hand_schatten.png"
        self.chunkpage.back_image = "data/pictures/mario_hand_schatten.png"
        self.aboutpage.back_image = "data/pictures/mario_hand_schatten.png"
        self.finishedpage.back_image = "data/pictures/mario_hand_schatten.png"
        self.homepage.deck_image = "data/pictures/deck_hallo.png"
        self.homepage.data_image = "data/pictures/data_button_stark.png"
        self.vocabfrontpage.start_image = "data/pictures/start_pixel.png"
        self.chunkpage.continue_image = "data/pictures/weiter_pixel.png"
        self.finishedpage.refresh_image = "data/pictures/deck_refresh.png"

    def set_random_line(self):
        line = random.choice(self.lines)
        self.pageone.line_image = line
        self.pagetwo.line_image = line

if __name__ == '__main__':
    HalloApp().run()