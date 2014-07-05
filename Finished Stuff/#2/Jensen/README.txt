					The 8-puzzle 
	(also capable of 15-puzzle, but runtime is very lengthy)

What is it?
	It's a simple search implementation in python using an 8-puzzle board (implemented with instances of BoardClass) and a module containing all searches. The board is passed to the search function, and what's returned is a list of all steps (in the form of BoardClass objects) from the starting board to the goal. 

----------------------------------------------------------------

Files:
--EightPuzzle_Main.py
--BoardClass.py
--my_searches.py

----------------------------------------------------------------

Main Function:
	Imports files and combines functionality. Test-calling program, nothing more.

Board Class:
	File containing all classes to do with the board itself and the functionality contained therein. Constructed w/o data but methods provided for copying/randomly initializing.

My Searches:
	Module containing A* (AStar) and Best First (BestFirstSearch) searches. Called with a board to complete the 8-puzzle and return a list containing boards of all the interim steps.

----------------------------------------------------------------

Example implementation:

b = BoardClass()
b.initialize_puzzle_board(3, hType=1, random=True, diff=None)
	     #width of board ^
solution = AStar(b)