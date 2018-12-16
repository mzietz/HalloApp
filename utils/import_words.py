


class ImportWords:
	def __init__(self):
		self.newLibrary = "German1000"
		self.txt = "german_lib"
		self.liste = []

	def loadWordsfromTxt(self):
		with open(self.txt) as f:
			for line in f:
				line = line.split("	")
				del line[0]
				for x in line:
					line[1] = line[1].rstrip("\r\n")
				line = [x.strip(' ') for x in line]
				line.insert(1,":")
				line.insert(3,":")
				line.insert(4,"0")
				for x in line:
					line = ''.join(line)
#				line = line[1,2]
				self.liste.append(line)
			print(self.liste)

	def saveWordsfromTxt(self):
#		print(self.deck[0].card[0].question+":"+self.deck[0].card[0].answer+":"+self.deck[0].card[0].learnedStatus+":"+self.deck[0].card[0].timeUntilShow)
		with open(self.newLibrary, "w") as f:
			f.write("D!"+self.newLibrary+":"+str(0)+ "\n")
			for x in self.liste:
				f.write(x+"\n")
			f.close()
		print("saved")


if __name__ == '__main__':
	myWords = ImportWords()
	myWords.loadWordsfromTxt()
	myWords.saveWordsfromTxt()