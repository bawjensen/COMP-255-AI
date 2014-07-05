from random import randint, shuffle

#======================================================================

class BoardClass(object):
	"""Board of N x N dimensions, to solve the (n**2 - 1)-puzzle"""
	goal = []
	goalTileLocations = {}

#======================================================================

	def __init__(self, hType=1):
		"""
		Constructor. Takes optional argument of heuristic type, which is settable and
		overrideable in various places.
		Creates various data members for later use, such as parent, the list for the board, 
		number of steps from original board to this one, etc.
		"""
		self.parent = None
		self.board = []
		self.hType = hType
		self.steps = 0

#======================================================================

	def __eq__(self, other):
		"""
		Uses the hashed boardList (as a string) to determine equality. 
		"""
		if self.eqHash == other.eqHash:
			return True
		else:
			return False

#======================================================================

	def __str__(self):
		"""
		Creates the list to return, appends the necessary information with formatting
		and returns that. Variable size for 8- or 15-puzzle
		"""
		outStr = ""
		outStr += "Heuristic Level: " + str(self.heuristic)
		outStr += "\n-" + "-----"*self.n
		for row in self.board:
			tempStr = ("\n|" + " %2d |" * self.n)
			outStr += tempStr % tuple(row)
			outStr += "\n-" + "-----"*self.n

		return outStr

#======================================================================

	def set_type(self, hType=1):		
		"""
		A simple method to set the type of the board's heuristic explicitly, instead
		of inside initialize_puzzle_board or the constructor.
		"""
		# Board Types:
		# 0 - Displaced Tiles Heuristic
		# 1 - Manhatten Distance Heuristic
		self.hType = hType

#======================================================================

	def initialize_puzzle_board(self, n=3, hType=1, random=True, diff=None):
		"""
		Method to create the first board, the one to be passed to the search function.
		Has the option to randomly create the board or not, and if not then which difficulty
		to choose. Defaults to a random board, of heuristic type manhatten distance.
		"""
		self.n = n

		# While loop to continuously create random boards until a solvable one is made.
		boardList = [x for x in range(n**2)]
		while random:
			shuffle(boardList)

			if self.generated_solvable(boardList):
				print "Found something solvable:", boardList
				break # From outer While-True

		# If statements to use non-random, burnt-in boards of various difficulties.
		if not random and n == 3:
			if diff == 0:
				boardList = [3,1,2,4,7,5,6,8,0]
			elif diff == 1:
				boardList = [3,2,5,4,1,8,6,0,7]
			elif diff == 2:
				boardList = [1,0,6,5,7,4,2,3,8]

		elif not random and n == 4:
			if diff == 0:
				boardList = [4,1,2,3,5,0,6,7,8,9,10,11,12,13,14,15]

		# Location of 0 (the empty tile) in the flat list.
		locZero = boardList.index(0)

		# Using floor division and modulo to attain the nested location of the 0
		self.x = locZero // self.n
		self.y = locZero % self.n

		# Looping over the flat list and appending it, creating the nested list that is the final board
		for i in range(self.n):
			i1, i2 = self.n*i, self.n*(i+1)
			self.board.append(boardList[i1:i2])

		# Double checking that we determined 0's position correctly.
		assert( self.board[self.x][self.y] == 0 )

		# Generate the goal (class variable) for the board based on size
		self.generate_goal()
		# Generates the heuristic value for this first board.
		self.generate_heuristic()
		# Generates the hash value for __eq__ from the board.
		self.eqHash = hash(str(self))

#======================================================================

	def generate_goal(self):
		"""
		Creates a simple nested list of what the goal should look like.
		"""
		# Creates a flat list of correct values
		tempList = [x for x in range(self.n**2)]

		# Nests those lists into a NxN
		BoardClass.goal = [tempList[self.n*i:self.n*(i+1)] for i in range(self.n)]

		# Creates a dictionary for the intended location of any specific tile. Used in
		# Manhatten Distance calculation.
		for i in range(self.n**2):
			row = i // self.n
			col = i % self.n
			BoardClass.goalTileLocations[i] = [row, col]

#======================================================================

	def generated_solvable(self, numList):
		"""
		Checks using an algorithm incorporating the number of inversions (times that a tile
		is in front of one smaller than it) to see if a list of numbers (representing a board)
		is solvable.
		"""
		# Counts inversions
		numInversions = 0
		for i in range(len(numList)):
			num = numList[i]
			for secNum in numList[i+1:]:
				# Checks if the first number is greater - ignoring the 0.
				if num > secNum and secNum != 0 and num != 0:
					numInversions += 1

		inversionsEven = numInversions % 2 == 0
		widthEven = self.n % 2 == 0
		# Checks to see if the 0 is on an odd row (from the bottom)
		blankOddRow = ( ((self.n**2-1)-numList.index(0)) // self.n ) % 2 == 0

		# Actual algorithm.
		if (not(widthEven) and inversionsEven) or (widthEven and (blankOddRow == inversionsEven)):
			result = True
		else:
			result = False

		return result

#======================================================================

	def copy(self):
		"""
		copyCTOR to create a new board with the same info as the one that this method is called on.
		Used in creating children.
		"""
		newBoard = BoardClass()

		for row in self.board:
			newBoard.board.append(row[:])
		newBoard.x = self.x
		newBoard.y = self.y
		newBoard.heuristic = self.heuristic
		newBoard.n = self.n
		newBoard.hType = self.hType
		newBoard.steps = self.steps

		return newBoard

#======================================================================

	def generate_possible_moves(self):
		"""
		Returns a list of the moves that any board can make.
		Used in creating children.
		"""
		# Moves:
		# 0 - North
		# 1 - East
		# 2 - South
		# 3 - West

		moves = []

		if self.x != 0:
			moves.append(0)
		if self.y != self.n-1:
			moves.append(1)
		if self.x != self.n-1:
			moves.append(2)
		if self.y != 0:
			moves.append(3)

		return moves		

#======================================================================

	def make_move(self, direction):
		"""
		Uses direction to swap tiles as if the empty tile had been slid north (0), east (1), etc.
		Used in creating children.
		"""
		if direction == 0:
			self.board[self.x][self.y], self.board[self.x-1][self.y] = self.board[self.x-1][self.y], self.board[self.x][self.y]
			self.x -= 1

		elif direction == 1:
			self.board[self.x][self.y], self.board[self.x][self.y+1] = self.board[self.x][self.y+1], self.board[self.x][self.y]
			self.y += 1

		elif direction == 2:
			self.board[self.x][self.y], self.board[self.x+1][self.y] = self.board[self.x+1][self.y], self.board[self.x][self.y]
			self.x += 1

		elif direction == 3:
			self.board[self.x][self.y], self.board[self.x][self.y-1] = self.board[self.x][self.y-1], self.board[self.x][self.y]
			self.y -= 1

#======================================================================

	def make_children(self):
		"""
		Incorporates various methods to create all the possible children of any given board.
		"""
		children = []

		posMoves = self.generate_possible_moves()

		for direction in posMoves:
			newChild = self.copy()

			newChild.make_move(direction)
			newChild.steps += 1
			newChild.generate_heuristic()
			newChild.eqHash = hash(str(newChild))

			children.append(newChild)

		return children

#======================================================================

	def is_goal(self):
		"""
		Simple method to test if the given board matches the goal board. Breaks as soon as
		a number doesn't match.
		"""
		for row in range(self.n):
			for col in range(self.n):
				if self.board[row][col] != BoardClass.goal[row][col]:
					return False

		return True

#======================================================================

	def back_trace(self, finalList=[]):
		"""
		Method used in returning the final list of moves from start to goal. Goes through the parent
		pointers in each of the Boards.
		"""
		if self.parent != None:
			self.parent.back_trace()
			finalList.append(str(self))
			return finalList
		else:
			finalList.append(str(self))
			return finalList


#======================================================================

	def generate_heuristic(self):
		"""
		Simple function to call to generate a heuristic for a given board.
		Calls two separate functions - for readability.
		"""
		if self.hType == 0:
			self.use_displaced_heur()

		elif self.hType == 1:
			self.use_manhatten_heur()

#======================================================================

	def use_displaced_heur(self):
		"""
		Heuristic totaling the number of tiles out of place.
		"""
		displacedTiles = 0

		for row in range(self.n):
			for col in range(self.n):
				if self.board[row][col] != BoardClass.goal[row][col]:
					displacedTiles += 1

		self.heuristic = displacedTiles

#======================================================================

	def use_manhatten_heur(self):
		"""
		Heuristic totaling the straight distance from start to goal of every tile, of physics were to
		be ignored.
		"""
		distance = 0

		for row in range(self.n):
			for col in range(self.n):
				intendedX, intendedY = BoardClass.goalTileLocations[self.board[row][col]]
				distance += (abs(row - intendedX) + abs(col - intendedY))

		self.heuristic = distance

#======================================================================