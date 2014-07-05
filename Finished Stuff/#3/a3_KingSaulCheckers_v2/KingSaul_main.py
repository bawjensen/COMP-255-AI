
from Board import *
from King  import *

#=====================================================    
def main():
    
    print "Welcome to King Saul Checkers! [5x5, two Kings each]"
    
    # test default CTOR
    B = Board()
    print B
    
    # test setting up an initial board
    B.initializeBoard()
    print B
    
    # test iterating over all the pieces (kings) on the board
    # whichKing is hash: key: name, value: King object
    for nextKing in B.whichKing.keys():
	print B.whichKing[nextKing]
	
	
    
    # test making (potential) moves of each King on board B
    nextMoves = []
    for moveThisKing in B.whichKing.keys():
	newBoards = B.getNextMoves( B.whichKing[moveThisKing] )
	
	print "----------------------------------------------"
	print "Potential Moves for King: ", moveThisKing
	for nextBoard in newBoards:
	    print "\tFROM", B.whichKing[ moveThisKing ].chinookNum, "TO", nextBoard.whichKing[ moveThisKing ].chinookNum
    
    
    
    

    
    
#-----------\
# START HERE \
#-----------------------------------------------------------	
if __name__ == '__main__':
	main()

#-----------------------------------------------------
