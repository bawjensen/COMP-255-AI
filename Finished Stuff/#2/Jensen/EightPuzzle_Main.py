from BoardClass import *
from my_searches import *

# implemented in Python v2.x


#=====================================================    
def main():
	# Create instance
	b = BoardClass()

	# Generation of board for starting board. First parameter is width.
	# diff = 0, 1 or 2
	b.initialize_puzzle_board(3, hType=1, random=True, diff=None)

	# For loop for multiple runs (timing).
	n = 1
	for i in range(n):
		solution = AStar(b)

	print "Avg Moves:", float(len(solution)) / float(n)
	print "Solved %i times." % n


#-----------\
# START HERE \
#-----------------------------------------------------------	
if __name__ == '__main__':
	main()
#-----------------------------------------------------------