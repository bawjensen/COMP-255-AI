from xml.dom import minidom       
import os
import re

# uses python v2.x

"""
===============================================================
This code parses an XML version of the entire collection
of Federalist Papers into unique folders for each author
(Madison, Hamilton, Jay), as well two additional folders
for (Disputed, CoAuthor).

Uses Python (XML) DOM (Document Object Model) to find
<div><text>....</text></div> tags to locate each of the
85 Federalist Papers.

thanks to Matt Jockers, Stanford for XML version

3/8/2011 (mdl)
===============================================================
"""

def main():

    xmldoc = minidom.parse('gutenfeder.xml')  

    
    # each Federalist Paper is in its own <div> tag
    for nextDIV in xmldoc.getElementsByTagName('div'):
   
	# each paper has title, author, and text tags
	for e in nextDIV.childNodes:
	    
	    if e.nodeType == e.ELEMENT_NODE and e.localName == "title":
		print "%s -- " % e.childNodes[0].data
		#exit()
		title = e.childNodes[0].data
		
	    if e.nodeType == e.ELEMENT_NODE and e.localName == "author":
		print e.childNodes[0].data
		author = e.childNodes[0].data
		
	    actualText = ""
	    if e.nodeType == e.ELEMENT_NODE and e.localName == "text":
		
		# traverse thru and snag text in each <p> tag
		for nextP in e.childNodes:
		    if nextP.nodeType == e.ELEMENT_NODE and nextP.localName == "p":
			actualText = actualText + " " + nextP.childNodes[0].data
		
		# now save text to its own file in the appropriate folder
		saveFederalistPaper( title, author, actualText )

	    
# ===============================================================
def saveFederalistPaper( title, author, actualText):
    
    """
    open new file for this Federalist Paper;
    store in /Federalist_Papers/AUTHOR/ directory; 
    also tack on first initial of author to mangled filename, 
    for example:
    ./Federalist_Papers/HAMILTON/FED_84_H.txt
    """
    
    newDir = "Federalist_Papers" 
    # make subdir if not there yet
    if not os.path.exists(newDir):
        os.mkdir(newDir)
    
    # start crafting (mangling) name for new directory
    newDir = newDir + "/" + author
    
    # make subdir if not there yet
    if not os.path.exists(newDir):
        os.mkdir(newDir)
	
	
    # tack first letter of "known" author to filename
    REauthorInitial = re.compile('^(.)')
    match = REauthorInitial.match(author)
    # group(0) is entire pattern matched; group(1) is first letter
    authorInitial = match.group(1)
    
    # title could be:  FEDERALIST No. 82   
    # so just save number of paper from group(1)
    REpaperNum = re.compile('^FEDERALIST.*No\.\s+(\d+)$')
    match = REpaperNum.match(title)
    # group(0) is entire pattern matched; group(1) is first ()'s
    filename = newDir + "/FED_" + str( match.group(1) ) + "_" + authorInitial + ".txt"
    
    #print filename
    FILE = open(filename, "w")

    FILE.write(actualText)
    
    FILE.close()
 


	    
	    
	    

# ===============================================================
if __name__ == '__main__':
	main()
# ===============================================================