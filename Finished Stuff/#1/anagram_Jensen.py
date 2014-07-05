from string import ascii_lowercase
from time import time
from re import match

class Trie():
    """
    Data structure to hold the initial dictionary imported from a file. When
    initialized, it calls self.start_up() to construct the inital node to
    the alphabet seed nodes. 
    """
    def __init__(self, data=[]):
        self.nodeList = data
        self.start_up()
        self.anagramsFound = []
    
    """
    Called by __init__(), it simply starts the Trie with a ROOT node with child
    nodes of all 26 letters of the alphabet. It then marks a (the [0] slot) and
    i ([8]) as complete words.
    """
    def start_up(self):
        self.rootNode = TrieNode("ROOT")
        for let in ascii_lowercase:
            self.rootNode.add_child(let)
        
        self.rootNode.children[0].isWord = True
        self.rootNode.children[8].isWord = True
        
    """
    Method to construct the Trie, it accepts a string in and will add nodes to
    the trie as needed for later iterating through and finding words. It accepts
    one argument on initial call, the string, and on successive calls (recursive)
    it will accept a second argument, the "parent" or baseNode, which defaults
    to a string for an 'if' test, (as python doesn't allow the passing in of
    self.rootNode itself as a default).
    """
    def add_word(self, string, baseNode="none"):
        # For defaulting to the rootNode of the entire trie
        if baseNode == "none":
            baseNode = self.rootNode
            
        # If reached the depth of the recursion of adding a word. Marks the end
        # spot with isWord and backs out of the recursion.
        if len(string) == 0:
            baseNode.isWord = True
            return
        
        # Iterates through the children nodes and recusively calls add_word with
        # that node as a new parent - breaks out of the iteration if it finds
        # a complete match, because otherwise it will create a new node (the else)
        for childNode in baseNode.children:
            if string[0] == childNode.item:
                self.add_word(string[1:], childNode)
                break
        else:
            self.add_word(string[1:], baseNode.add_child(string[0]))
            
            
    def anagram_finder(self, remainingLetters, stringSoFar="", wordsSoFar=[], children="none"):
        """
        The counter-part method to add_word, this function searches through the 
        trie to construct the anagrams. It stores potentials in a list, and
        passes values instead of references by [:].
        Once a complete match is found (all the letters of the input string are
        used up) the result is printed to the console with a number of how many
        have been found before.
        
        Accepts one argument on initial call, and the rest are for recursion calls, 
        with default values for the first run.
        """
        
        # Another defaulting trick to allow for self.rootNode
        if children == "none":
            children = self.rootNode.children
        
        # Iterates through the children
        for child in children:
            
            # If the child matches something already had
            if child.item in remainingLetters:
                
                # Removes that letter (storing in new variable to preserve the
                # old for successive loopings of the above "for")
                newLetters = remainingLetters.replace(child.item, "", 1)
                # Adds the letter onto the potential word string (storing same)
                newStringSoFar = stringSoFar + child.item
                
                # If the recursion has reached a node marked as the end of a word
                # and there are no more letters to pull from, a complete anagram
                # has been found - prints to console with formatting and
                # increments the number found so far
                if child.isWord and newLetters == "":
                    
                    # If to remove duplicates (only prints anagrams with words
                    # in alphabetical order)
                    if len(wordsSoFar) > 0 and wordsSoFar[-1][0] < newStringSoFar[0]:
                        
                        # Adds the final word to the now-completed list
                        wordsSoFar += [newStringSoFar]
                        # Formatted printing
                        self.anagramsFound.append(wordsSoFar)
                        
                    # Same with the if directly above, handles the case of a
                    # single-word anagram
                    elif len(wordsSoFar) == 0:
                        
                        wordsSoFar += [newStringSoFar]
                        self.anagramsFound.append(wordsSoFar)

                
                # If the child is the end of a word but the letters have not
                # run out yet, then recursively call with the word added to list
                elif child.isWord:
                    
                    # If statement to remove duplicates
                    if len(wordsSoFar) > 0 and wordsSoFar[-1][0] < newStringSoFar[0]:
                        # RECURSION CALL - end of word
                        self.anagram_finder( newLetters, wordsSoFar=(wordsSoFar[:]+[newStringSoFar]) )
                    
                    # If statement to remove duplicates
                    elif len(wordsSoFar) == 0:
                        # RECURSION CALL - end of word
                        self.anagram_finder( newLetters, wordsSoFar=(wordsSoFar[:]+[newStringSoFar]) )
                    
                    # RECURSION CALL - node is the end of a word, but not treated
                    # as such (i.e. with "a", want it to find "and" as well)
                    self.anagram_finder(newLetters, newStringSoFar, wordsSoFar[:], child.children)
                
                else: # If node is not ending a word:
                    # RECURSION CALL - usual recursion call
                    self.anagram_finder(newLetters, newStringSoFar, wordsSoFar[:], child.children)
                    
                    
class TrieNode(object):
    """
    Node class for an instance of Trie. Each node stores its data (a letter),
    a list of its children (TrieNodes) and whether that node is the end of some
    word. Initializes with all three defaulting to None/empty/False.
    """
    def __init__(self, data=None):
        self.item = data
        self.children = []
        self.isWord = False
        
    
    """
    Called by the Trie when needing to add a new node to the trie. Can accept
    a string or a TrieNode as an argument and converts the first to the second]
    before appending it to the parent node's list of children nodes.
    NOTE: Does nothing and returns nothing if arguments invalid.
    """
    def add_child(self, node):
        # If it's a node already, just append.
        if type(node) == type(TrieNode):
            self.children.append(node)
            return addedNode
        
        # If it's a string, create a new TrieNode and append that.
        elif type(node) == str:
            addedNode = TrieNode(node)
            self.children.append(addedNode)
            return addedNode
        
        
class Anagram(object):
    """
    Anagram class as an API for the Trie and TrieNode classes. Initializes
    with a stripped-down copy of the input word and the filename stored. It then
    calls make_trie on itself.
    """
    def __init__(self, sourceWord, fileName):
        self.word = self.strip_and_clean(sourceWord)
        self.fileName = fileName
        
        self.make_trie()
        
    """
    Called in __init__(), it uses the self.fileName variable to pass the
    dictFile, word by word, to the Trie.add_word() method. The Trie instance is
    also first initialized in this method.
    """
    def make_trie(self):
        self.dictTrie = Trie()
        
        f = open(self.fileName, 'r')
        
        for line in f:
            self.dictTrie.add_word(self.strip_and_clean(line))
        
        f.close()
            
    """
    A simple method to take in a string and remove everything unwanted from it,
    converting it to lowercase and returning the new string.
    """
    def strip_and_clean(self, string):
        undesiredChars = [" ", "\n"]
        string2 = ""
        for letter in string:
            if letter not in undesiredChars:
                string2 += letter.lower()
                    
        return string2
    
    """
    An API method to allow for the input of a word for which to find the anagrams.
    All output printing is done inside anagram_finder.
    """
    def find_anagrams(self):
        self.dictTrie.anagram_finder(self.strip_and_clean(self.word))
        
    """
    Simple error method to clear up any confusion upon call.
    """
    def findAnagrams(self):
        print "Sorry, the Python style guide says to use under_scores to denote object methods."
        print "The method for your instance of Anagram is .find_anagrams()."

    def get_anagrams(self):
        return self.dictTrie.anagramsFound