class Board(object):
	OPENSPOT = u"\u2591\u2591"
	CLOSEDSPOT = u"\u2588\u2588\u2588\u2588\u2588\u2588"
	OPENFILLER = u"\u2591\u2591"

	def __init__(self, width, num_pieces, humanFirst = True):
		if width % 2 != 0:
			raise ValueError("Width of board has to be even")

		self.width = width
		self.num_pieces = num_pieces

		num_board_spaces = width**2
		self.num_c_positions = num_board_spaces // 2

		self.c_board = {}
		self.moves_by_c_num = {}
		self.jumps_by_c_num = {}
		self.computer_positions = []
		self.human_positions = []
		self.human_turn = humanFirst
		self.game_over = False


	def initialize_board(self):
		for i in range(self.num_c_positions):
			self.c_board[i+1] = Board.OPENSPOT

		for i in range(self.num_pieces):
			i += 1

			self.c_board[i] = "H" + str(i)
			self.human_positions.append(i)

			comp_pos = self.num_c_positions + 1 - i
			self.c_board[comp_pos] = "C" + str(i)
			self.computer_positions.append(comp_pos)

		self.generate_c_info()

	def generate_c_info(self):
		c_num = 0
		c_nums_per_row = self.width / 2

		for row in range(self.width, 0, -1):
			for col in range(c_nums_per_row, 0, -1):
				c_num += 1
				self.moves_by_c_num[c_num] = []

				north_check = c_num + c_nums_per_row <= self.num_c_positions
				east_check = (c_num - 1 - c_nums_per_row) % self.width != 0
				south_check = c_num - c_nums_per_row >= 1
				west_check = (c_num - c_nums_per_row) % self.width != 0

				if north_check and east_check:
					self.moves_by_c_num[c_num].append([c_num + (c_nums_per_row + 0 - (row % 2)), "NE"])
				if east_check and south_check:
					self.moves_by_c_num[c_num].append([c_num - (c_nums_per_row + 0 + (row % 2)), "SE"])
				if south_check and west_check:
					self.moves_by_c_num[c_num].append([c_num - (c_nums_per_row - 1 + (row % 2)), "SW"])
				if west_check and north_check:
					self.moves_by_c_num[c_num].append([c_num + (c_nums_per_row + 1 - (row % 2)), "NW"])


		c_num = 0

		for row in range(self.width, 0, -1):
			for col in range(c_nums_per_row, 0, -1):
				c_num += 1
				self.jumps_by_c_num[c_num] = []

				north_check = c_num + 2*c_nums_per_row <= self.num_c_positions
				east_check = (c_num - 1) % c_nums_per_row != 0
				south_check = c_num - 2*c_nums_per_row >= 1
				west_check = (c_num) % c_nums_per_row != 0

				if north_check and east_check:
					self.jumps_by_c_num[c_num].append([c_num + (self.width - 1), "NE"])
				if east_check and south_check:
					self.jumps_by_c_num[c_num].append([c_num - (self.width + 1), "SE"])
				if south_check and west_check:
					self.jumps_by_c_num[c_num].append([c_num - (self.width - 1), "SW"])
				if west_check and north_check:
					self.jumps_by_c_num[c_num].append([c_num + (self.width + 1), "NW"])


	def isJumping(self, start, end, direction):
		jumping = False

		if abs(start - end) >= (self.width / 2 + 2):
			if direction == None:
				for slot in self.jumps_by_c_num[start]:
					if slot[0] == end:
						direction = slot[1]

			jumping = True

		return jumping, direction


	def movePiece(self, start, end, direction=None):
		if self.c_board[start] == Board.OPENSPOT:
			#raise ValueError("Move attempted on space with no piece.")
			print "Move attempted on space with no piece."
		if self.human_turn ^ (self.c_board[start][0] == "H"):
			raise ValueError("Human move attempted on non-human turn.")
			#print "Human move attempted on non-human turn or vice versa."

		moveSuccessful = False
		jumping, direction = self.isJumping(start, end, direction)

		if not jumping:
			if end in [slot[0] for slot in self.moves_by_c_num[start]] and self.c_board[end] == Board.OPENSPOT:
				self.c_board[start], self.c_board[end] = self.c_board[end], self.c_board[start]
				moveSuccessful = True

		elif jumping:
			if [end, direction] in self.jumps_by_c_num[start]:
				jumpable = False
				inbetween_index_from_dir = [slot[1] for slot in self.moves_by_c_num[start]].index(direction)
				c_num_of_inbetween = self.moves_by_c_num[start][inbetween_index_from_dir][0]

				if (self.c_board[c_num_of_inbetween][0] == "H" and self.c_board[start][0] == "C") or (self.c_board[c_num_of_inbetween][0] == "C" and self.c_board[start][0] == "H"):
					print "GOT HERE"
					jumpable = True

				if jumpable and self.c_board[end] == Board.OPENSPOT:

					if self.c_board[ c_num_of_inbetween ][0] == "C":
						self.computer_positions.remove( c_num_of_inbetween )
					if self.c_board[ c_num_of_inbetween ][0] == "H":
						self.human_positions.remove( c_num_of_inbetween )

					self.c_board[ c_num_of_inbetween ] = Board.OPENSPOT

					self.c_board[start], self.c_board[end] = self.c_board[end], self.c_board[start]
					moveSuccessful = True


		if moveSuccessful:
			self.human_turn = not self.human_turn

			if self.c_board[end][0] == "C":
				self.computer_positions[self.computer_positions.index(start)] = end
			elif self.c_board[end][0] == "H":
				self.human_positions[self.human_positions.index(start)] = end


		if not (self.computer_positions and self.human_positions):
			self.game_over = True

		return moveSuccessful


	def copy(self):
		new_board = Board(self.width, self.num_pieces)

		for key, value in self.c_board.items():
			new_board.c_board[key] = value

		for key, value in self.moves_by_c_num.items():
			new_board.moves_by_c_num[key] = value

		for key, value in self.jumps_by_c_num.items():
			new_board.jumps_by_c_num[key] = value

		new_board.human_turn = self.human_turn
		new_board.computer_positions = self.computer_positions[:]
		new_board.human_positions = self.human_positions[:]

		return new_board

	def generateChildren(self):
		self.children = []

		if not self.human_turn:
			for c_pos in self.computer_positions:
				for possible_move in self.jumps_by_c_num[c_pos]:
	 				new_board = self.copy()

					if new_board.movePiece(c_pos, possible_move[0], possible_move[1]):
						self.children.append(new_board)

				for possible_move in self.moves_by_c_num[c_pos]:
					new_board = self.copy()

					if new_board.movePiece(c_pos, possible_move[0]):
						self.children.append(new_board)
		elif self.human_turn:
			for c_pos in self.human_positions:
				for possible_move in self.jumps_by_c_num[c_pos]:
	 				new_board = self.copy()

					if new_board.movePiece(c_pos, possible_move[0], possible_move[1]):
						self.children.append(new_board)

				for possible_move in self.moves_by_c_num[c_pos]:
					new_board = self.copy()

					if new_board.movePiece(c_pos, possible_move[0]):
						self.children.append(new_board)

	def __str__(self):
		switcher = False
		buff = ""
		c_num = 0

		filler_strip = ""
		filler_strip += Board.CLOSEDSPOT

		for i in range(self.width / 2):
			filler_strip += Board.OPENFILLER*3
			filler_strip += Board.CLOSEDSPOT

		c_num_strip = ""
		c_num_strip += Board.CLOSEDSPOT

		for i in range(self.width / 2):
			c_num_strip += Board.OPENFILLER + "XX" + Board.OPENFILLER
			c_num_strip += Board.CLOSEDSPOT

		for row in range(self.width):
			switcher = not switcher
			row_str = ""
			row_str += Board.CLOSEDSPOT
			temp_str_2 = c_num_strip

			for i in range(self.width / 2):
				c_num += 1
				row_str += Board.OPENFILLER + self.c_board[self.num_c_positions + 1 - c_num] + Board.OPENFILLER
				row_str += Board.CLOSEDSPOT
				if c_num < 10:
					temp_str_2 = temp_str_2.replace("XX", str(self.num_c_positions+1-c_num), 1)
				else:
					temp_str_2 = temp_str_2.replace("XX", "0"+str(self.num_c_positions+1-c_num), 1)

			if switcher:
				row_str = row_str.rstrip(Board.CLOSEDSPOT)
				temp_str = filler_strip.rstrip(Board.CLOSEDSPOT)
				temp_str_2 = temp_str_2.rstrip(Board.CLOSEDSPOT)

			else:
				row_str = row_str.lstrip(Board.CLOSEDSPOT)
				temp_str = filler_strip.lstrip(Board.CLOSEDSPOT)
				temp_str_2 = temp_str_2.lstrip(Board.CLOSEDSPOT)

			buff += (temp_str + "\n")
			buff += (row_str + "\n")
			buff += (temp_str_2 + "\n")

		return buff.encode("utf-8")