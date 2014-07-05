#from Board import *

class King(object):
    """one King object"""
    
    # class members (all instances use this same values)    
    CHINOOK_N = {}
    # for converting [x][y] locations to Chinook number
    CHINOOK_N[55] = 1
    CHINOOK_N[53] = 2
    CHINOOK_N[51] = 3
    
    CHINOOK_N[44] = 4
    CHINOOK_N[42] = 5
    CHINOOK_N[40] = 6
    
    CHINOOK_N[35] = 7
    CHINOOK_N[33] = 8
    CHINOOK_N[31] = 9
    
    CHINOOK_N[24] = 10
    CHINOOK_N[22] = 11
    CHINOOK_N[20] = 12
    
    CHINOOK_N[15] = 13
    CHINOOK_N[13] = 14
    CHINOOK_N[11] = 15
    
    CHINOOK_N[04] = 16
    CHINOOK_N[02] = 17
    CHINOOK_N[00] = 18
    
    

    
	
    #=====================================================         
    def __init__(self, setName, setX, setY):
        """CTOR
        """
        
        self.alive = True
        
        self.name = " "+setName+" "    # e.g., " mK1 ", " hK2 "
        self.who = setName[0]          # e.g., to tell if 'm' or 'h'
        self.X = setX
        self.Y = setY
        self.chinookNum = King.CHINOOK_N[ (setX*10) + setY]
        
        
        
        
    #=====================================================         
    def __str__(self):
        
        if (self.alive): 
		k = "{0:s} at [{1:d},{2:d}] [Chinook: {3:d}]".format(self.name, self.X, self.Y, self.chinookNum)
        return k
        
    #=====================================================          
    def copyCTOR(self):
        
        newKing = King( self.name, self.X, self.Y )
        newKing.alive = self.alive        
        #newKing.name = self.name
        newKing.who = self.who
        #newKing.X = self.X
        #newKing.Y = self.Y
        newKing.chinookNum = self.chinookNum
        
        return newKing
