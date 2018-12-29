#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver

# ca 12 sekunden pro vokabel

ger_list = []

with open("raw_data/A1Sonstiges.txt") as f:
	for line in f:
#		line = line.split(" ")
#		line = line[1]
#		if line[-1] == ",":
#			line = line[:-1]
		ger_list.append(line)


kor_list = []

for i, vocab in enumerate(ger_list):
	print "Vocab:" +vocab
	browser = webdriver.Firefox(executable_path=r'//home/max/venv/geckodriver-v0.23.0-linux64/geckodriver')
	url = 'http://dict.naver.com/dekodict/#/search?query='+vocab
	browser.get(url)

	innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
	browser.close()
	soup = BeautifulSoup(innerHTML, 'html.parser')
	kor = soup.find('span', attrs={'class': 'ellipsis'})
	try:
		kor = kor.text.split()
		for x in kor:
			x = x.rstrip()
		kor = " ".join(kor)
		print kor
		kor_list.append(kor)
	except:
		kor_list.append("Error")
	with open('A1Sonstiges_kor.json', 'w') as fd:
		json.dump(kor_list, fd)