import os
import string

def makeFeatures(s):
	featDict = {}
	wordList = s.split(" ")

	for word in wordList:
		word = cleanWord(word)

		if word in featDict.keys():
			featDict[word] += 1
		else:
			featDict[word] = 1

	return featDict

def cleanWord(s):
	return s.translate(string.maketrans("", ""), str(string.punctuation[:6] + string.punctuation[7:])).lower()

def findAllWords(dictionaries):
	buffWords = []

	for dictionary in dictionaries:
		for word in dictionary:
			if word not in buffWords:
				buffWords.append(word)

	return buffWords

def csvOutputWordRows(buffStr, words, dictionaries):
	for word in words:
		buffStr += word

		for dictionary in dictionaries:
			if word in dictionary:
				buffStr += ("," + str(dictionary[word]))
			else:
				buffStr += (",0")

		buffStr += "\n"

	return buffStr
		

def main():
	folder = os.path.join("""Path to .xml source files here""")

	paperFeatureDicts = []
	paperList = []
	buffStr = "Word,"

	for root, dirs, files in os.walk(folder):
		if not dirs:
			for f in files:
				with open(os.path.join(root, f)) as current_file:
					fileString = ""
					for line in current_file:
						fileString += line.strip()

				paperFeatureDicts.append(makeFeatures(fileString))
				paperList.append(f)
				buffStr += (f + ",")
	buffStr += "\n"

	allWords = findAllWords(paperFeatureDicts)

	buffStr1 = csvOutputWordRows(buffStr, allWords, paperFeatureDicts)

	#with open("rawFeatureSet.csv", "w") as oFile:
	#	oFile.write(buffStr1)

	dictOfWordSetsByAuthor = {}
	for i in xrange(len(paperList)):
		paperName = paperList[i]
		authorInitial = paperName[paperName.find(".")-1:paperName.find(".")]

		if authorInitial not in dictOfWordSetsByAuthor:
			dictOfWordSetsByAuthor[authorInitial] = set()

		dictOfWordSetsByAuthor[authorInitial] = dictOfWordSetsByAuthor[authorInitial].union(paperFeatureDicts[i].keys())

	wordsInAllAuthors = set(dictOfWordSetsByAuthor["D"])
	del dictOfWordSetsByAuthor["D"]

	for authorInital, wordSet in dictOfWordSetsByAuthor.iteritems():
		wordsInAllAuthors = wordsInAllAuthors.intersection(wordSet)

	buffStr2 = buffStr
	for word in wordsInAllAuthors:
		buffStr2 += word
		for featureSet in paperFeatureDicts:
			if word in featureSet:
				buffStr2 += ("," + str(featureSet[word]))
			else:
				buffStr2 += ",0"

		buffStr2 += "\n"

	with open("preprocessedByAuthorFeatureSet.csv", "w") as oFile:
		oFile.write(buffStr2)


if __name__ == "__main__":
	main()