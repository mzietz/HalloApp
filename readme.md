# 1 App

## A learning app for german learning koreans.

### App structure

The app is built within the kivy framework. It basically consists of three files:

1. main.py is handling all the app functionality.

2. jsonlibrary.py defines a flashcard deck class which also contains necessary functionality to manipulate the decks.

3. swipecards.kv is a file which defines all the visuals, buttons, and images, written in the kivy language.

### Utility

1. import_words.py helps parsing data and puts it into json format.

2. naverparser.py scrapes the naver german-korean dictionary for a translation of a given german word. While it automates the process of getting all the translation of a list of german vocabulary, it still requires manual corrections for alot of the translations. The reason for this is the sometimes questionable translations of the dictionary and also just selecting the first (most common?) translation of the given word, which is not always the targeting translation.

### Acknowledgments

Vocabulary was taken from official Goethe institute vocabulary list for language level A1, A2 and B1 respectivly. 