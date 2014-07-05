from string import ascii_lowercase
from time import time

class Trie():
    
    def __init__(self, data=[]):
        self.nodeList = data
        self.start_up()
        self.anagramsFound = 0
            
    def start_up(self):
        self.rootNode = TrieNode("ROOT")
        for let in ascii_lowercase:
            self.rootNode.add_child(let)
    
    def add_word(self, string, baseNode="none"):
        if baseNode == "none":
            baseNode = self.rootNode
            
        if len(string) == 0:
            baseNode.isWord = True
            return
        
        for childNode in baseNode.children:
            if string[0] == childNode.item:
                self.add_word(string[1:], childNode)
                break
        else:
            self.add_word(string[1:], baseNode.add_child(string[0]))
            
    def anagram_finder(self, remainingLetters, stringSoFar="", wordsSoFar=[], children="none"):
        if children == "none":
            children = self.rootNode.children
            
        for child in children:
            #if not ['a','e','i','o','u','y'] in remainingLetters and ['a','e','i','o','u','y'] not in stringSoFar:
            #    return
            
            if child.item in remainingLetters:
                newLetters = remainingLetters.replace(child.item, "", 1)
                if child.isWord and newLetters == "":
                    if len(wordsSoFar) > 0 and wordsSoFar[-1][0] < stringSoFar[0]:
                        wordsSoFar += [stringSoFar+child.item]
                        FILE.write(" ".join(wordsSoFar) + "\n")
                        self.anagramsFound += 1
                        
                    elif len(wordsSoFar) == 0:
                        wordsSoFar += [stringSoFar+child.item]
                        FILE.write(" ".join(wordsSoFar) + "\n")
                        self.anagramsFound += 1
                        
                    
                elif child.isWord:
                    try:
                        if wordsSoFar[0] == 'ceres':
                            pass
                    except:
                        pass
                        
                    if len(wordsSoFar) > 0 and wordsSoFar[-1][0] < stringSoFar[0]:
                        self.anagram_finder(newLetters, wordsSoFar=wordsSoFar[:]+[stringSoFar+child.item])
                    elif len(wordsSoFar) == 0:
                        self.anagram_finder(newLetters, wordsSoFar=wordsSoFar[:]+[stringSoFar+child.item])
                        
                    self.anagram_finder(newLetters, stringSoFar+child.item, wordsSoFar[:], child.children)
                
                else:
                    self.anagram_finder(newLetters, stringSoFar+child.item, wordsSoFar[:], child.children)
                    
class TrieNode(object):
    
    def __init__(self, data=None):
        self.item = data
        self.children = []
        self.isWord = False
        
    def add_child(self, node):
        if type(node) == type(TrieNode):
            self.children.append(node)
        elif type(node) == str:
            addedNode = TrieNode(node)
            self.children.append(addedNode)
            return addedNode
        
class Anagram(object):
    
    def __init__(self, sourceWord, fileName):
        self.word = self.strip_and_clean(sourceWord)
        self.fileName = fileName
        
        self.make_trie()
        #self.dictTrie.trie_print()
    
    def make_trie(self):
        self.dictTrie = Trie()
        
        f = open(self.fileName, 'r')
        
        for line in f:
            self.dictTrie.add_word(self.strip_and_clean(line))
            
    def strip_and_clean(self, string):
        undesiredChars = [" ", "\n"]
        string2 = ""
        for letter in string:
            if letter not in undesiredChars:
                string2 += letter.lower()
                    
        return string2
    
    def find_anagrams(self):
        self.dictTrie.anagram_finder(strip_and_clean(self.word))
        print self.dictTrie.anagramsFound
        

def main():
    a = Anagram("Google Search", "english.txt")
    
    a.find_anagrams()
    

def strip_and_clean(string):
    undesiredChars = [" ", "\n"]
    string2 = ""
    for letter in string:
        if letter not in undesiredChars:
            string2 += letter.lower()
            
    return string2
    
if __name__ == '__main__':
    iTime = time()
    
    FILE = open('anagramsForGoogleSearch.txt', 'w')
    
    main()
    print time() - iTime
    FILE.close()