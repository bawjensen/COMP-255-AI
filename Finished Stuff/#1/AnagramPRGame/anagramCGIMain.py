import cgi
import cgitb
import random
import pickle
import os
from time import time
cgitb.enable(display=0, logdir="/tmp")

from AnagramGame import *

print "Content-type:text/html\r\n\r\n"

form = cgi.FieldStorage()

#phrase = form.getvalue('phrase').lower()
phrase = "glaucoma"
fileName = "RunData.txt"

try:
	open(fileName, 'r')
	fileExists = True
except:
	fileExists = False

if phrase is not None and not fileExists:
	anagramsOfPhrase = Anagram(phrase, 'english.txt')

	anagramsOfPhrase.find_anagrams()

	anagramsList = anagramsOfPhrase.get_anagrams()

	print "<html>"
	print "<head>"
	print "<title>Anagram Finder</title>"
	print "</head>"
	print "<body>"
	print "<p>"

	print "Found %i anagrams of at least 4/5 the length of the original.<br>" % (len(anagramsList))

	print "</p>"
	print "</body>"
	print "</html>"

	with open(fileName, "w") as FOUT:
		FOUT.write( (str(time()) + "\n") ) 
		FOUT.write(phrase)
		for anagram in anagramsList:
			FOUT.write( "\n" + str(anagram) )

elif fileExists:

	with open(fileName, "r") as oldFile:
		tempList = []
		for line in oldFile:
			tempList.append(line.strip())

	oldTime = tempList[0]
	oldPhrase = tempList[1]
	anagramsList = tempList[2:]

	if phrase in anagramsList and phrase != oldPhrase:
		print "<br> %s matched in %f seconds! <br>" % (phrase.upper(), (time()-float(oldTime)))

	elif phrase == oldPhrase:
		print "<br> As if you could cheat that easily. <br>"

	else:
		print "<br> Not an anagram of the original. <br>"
		print "(At least according to my dictionary) <br>"


	os.remove(fileName)