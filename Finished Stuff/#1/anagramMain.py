import cgi
import cgitb
import random
cgitb.enable(display=0, logdir="/tmp")

from AnagramGame import *

print "Content-type:text/html\r\n\r\n"

form = cgi.FieldStorage()

#phrase = form.getvalue('phrase').lower()
phrase = "stipend"

if phrase is not None:
	anagramsOfPhrase = Anagram(phrase, 'english.txt')

	anagramsOfPhrase.find_anagrams()

	anagramsList = anagramsOfPhrase.get_anagrams()

	print "<html>"
	print "<head>"
	print "<title>Anagram Finder</title>"
	print "</head>"
	print "<body>"
	print "<p>"

	print "Found %i anagrams.<br>" % (len(anagramsList))
	if len(anagramsList) > 1:
		while True:
			anagram = " ".join(random.choice(anagramsList))
			if anagram != phrase:
				print anagram + "<br>"
				break

	print "</p>"
	print "</body>"
	print "</html>"