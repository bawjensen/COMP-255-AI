class Board(object):
	OPENSPOT = u"\u2591\u2591\u2591\u2591\u2591\u2591"
	CLOSEDSPOT = u"\u2588\u2588\u2588\u2588\u2588\u2588"
	EMPTY_SLOT = u"\u2591\u2591"
	moves_by_c_num = {}
	jumps_by_c_num = {}
	direction_from_coords = {}
	num_c_positions = {}
	edge_c_nums = []


	def __init__(self, width, humanFirst = True):
		if width % 2 != 0:
			raise ValueError("Width of board has to be even")

		self.width = width

		Board.num_c_positions = width**2 // 2

		self.c_board = {}
		self.computer_positions = []
		self.human_positions = []
		self.human_turn = humanFirst
		self.game_over = False
		

	def initialize_board(self, num_pieces=2):
		for i in range(1, Board.num_c_positions+1):
			self.c_board[i] = Board.EMPTY_SLOT

		for i in range(1, num_pieces+1):
			self.c_board[i] = "H" + str(i)
			self.human_positions.append(i)

			comp_pos = Board.num_c_positions + 1 - i
			self.c_board[comp_pos] = "C" + str(i)
			self.computer_positions.append(comp_pos)

		self.generate_c_info()

	def generate_c_info(self):
		c_num = 0
		c_nums_per_row = self.width / 2

		for row in range(self.width, 0, -1):
			for col in range(c_nums_per_row, 0, -1):
				c_num += 1
				Board.moves_by_c_num[c_num] = []

				north_check = c_num + c_nums_per_row <= Board.num_c_positions
				east_check = (c_num - 1 - c_nums_per_row) % self.width != 0
				south_check = c_num - c_nums_per_row >= 1
				west_check = (c_num - c_nums_per_row) % self.width != 0


				if north_check and east_check:
					move_to = c_num + (c_nums_per_row - 0 - (row % 2))
					Board.moves_by_c_num[c_num].append(move_to)
					Board.direction_from_coords[(c_num, move_to)] = "NE"

				if east_check and south_check:
					move_to = c_num - (c_nums_per_row + 0 + (row % 2))
					Board.moves_by_c_num[c_num].append(move_to)
					Board.direction_from_coords[(c_num, move_to)] = "SE"

				if south_check and west_check:
					move_to = c_num - (c_nums_per_row - 1 + (row % 2))
					Board.moves_by_c_num[c_num].append(move_to)
					Board.direction_from_coords[(c_num, move_to)] = "SW"

				if west_check and north_check:
					move_to = c_num + (c_nums_per_row + 1 - (row % 2))
					Board.moves_by_c_num[c_num].append(move_to)
					Board.direction_from_coords[(c_num, move_to)] = "NW"

				if not north_check:
					Board.edge_c_nums.append(c_num)
				if not east_check:
					Board.edge_c_nums.append(c_num)
				if not south_check:
					Board.edge_c_nums.append(c_num)
				if not west_check:
					Board.edge_c_nums.append(c_num)

		Board.edge_c_nums = set(Board.edge_c_nums)


		c_num = 0

		for row in range(self.width, 0, -1):
			for col in range(c_nums_per_row, 0, -1):
				c_num += 1
				Board.jumps_by_c_num[c_num] = []

				north_check = c_num + 2*c_nums_per_row <= Board.num_c_positions
				east_check = (c_num - 1) % c_nums_per_row != 0
				south_check = c_num - 2*c_nums_per_row >= 1
				west_check = (c_num) % c_nums_per_row != 0

				if north_check and east_check:
					jump_to = c_num + (self.width - 1)
					Board.jumps_by_c_num[c_num].append(jump_to)
					Board.direction_from_coords[(c_num, jump_to)] = "NE"

				if east_check and south_check:
					jump_to = c_num - (self.width + 1)
					Board.jumps_by_c_num[c_num].append(jump_to)
					Board.direction_from_coords[(c_num, jump_to)] = "SE"

				if south_check and west_check:
					jump_to = c_num - (self.width - 1)
					Board.jumps_by_c_num[c_num].append(jump_to)
					Board.direction_from_coords[(c_num, jump_to)] = "SW"

				if west_check and north_check:
					jump_to = c_num + (self.width + 1)
					Board.jumps_by_c_num[c_num].append(jump_to)
					Board.direction_from_coords[(c_num, jump_to)] = "NW"


	def movePiece(self, start, end, direction=None):
		if self.c_board[start] == Board.EMPTY_SLOT:
			print "ERROR: Start was an empty spot (%s)." % start
			return False
		if self.c_board[end] != Board.EMPTY_SLOT:
			return False

		move_success = False

		jumping = False	
		if abs(start - end) > (self.width / 2 + 1):
			jumping = True
			direction = Board.direction_from_coords[(start, end)]

		if jumping:
			jumped = False
			for pos_end in Board.moves_by_c_num[start]:
				if Board.direction_from_coords[(start, pos_end)] == direction:
					break

			if self.c_board[pos_end][0] == "H" and self.c_board[start][0] == "C":
				self.human_positions.remove(pos_end)
				self.c_board[pos_end] = Board.EMPTY_SLOT
				jumped = True

			elif self.c_board[pos_end][0] == "C" and self.c_board[start][0] == "H":
				#print "Jumped from %s to %s over %s." %(start, end, self.c_board[pos_end])
				self.computer_positions.remove(pos_end)
				self.c_board[pos_end] = Board.EMPTY_SLOT
				jumped = True

		if end in Board.moves_by_c_num[start] or end in Board.jumps_by_c_num[start]:
			if (jumping and jumped) or (not jumping):
				move_success = True

		if move_success:
			self.c_board[end] = self.c_board[start]
			self.c_board[start] = Board.EMPTY_SLOT

			self.human_turn = not self.human_turn

			if self.c_board[end][0] == "C":
				self.computer_positions.remove(start)
				self.computer_positions.append(end)
			elif self.c_board[end][0] == "H":
				self.human_positions.remove(start)
				self.human_positions.append(end)

		if not (self.computer_positions and self.human_positions):
			self.game_over = True

		return move_success


	def copy(self):
		new_board = Board(self.width, self.human_turn)

		for key, value in self.c_board.items():
			new_board.c_board[key] = value

		new_board.computer_positions = self.computer_positions[:]
		new_board.human_positions = self.human_positions[:]

		return new_board

	def generateChildren(self):
		self.children = []

		if self.human_turn:
			for c_num in self.human_positions:
				for possible_move in Board.jumps_by_c_num[c_num]:
	 				new_board = self.copy()

					if new_board.movePiece(c_num, possible_move):
						self.children.append(new_board)

				for possible_move in self.moves_by_c_num[c_num]:
					new_board = self.copy()

					if new_board.movePiece(c_num, possible_move):
						self.children.append(new_board)

		else:
			for c_num in self.computer_positions:
				for possible_move in Board.jumps_by_c_num[c_num]:
	 				new_board = self.copy()

					if new_board.movePiece(c_num, possible_move):
						self.children.append(new_board)

				for possible_move in self.moves_by_c_num[c_num]:
					new_board = self.copy()

					if new_board.movePiece(c_num, possible_move):
						self.children.append(new_board)

	def __str__(self):
		switcher = False
		buff = ""
		c_num = 0

		filler_strip = Board.CLOSEDSPOT
		for i in range(self.width / 2):
			filler_strip += Board.OPENSPOT + Board.CLOSEDSPOT

		c_num_strip = Board.CLOSEDSPOT
		for i in range(self.width / 2):
			c_num_strip += Board.EMPTY_SLOT + "XX" + Board.EMPTY_SLOT + Board.CLOSEDSPOT

		for row in range(self.width):
			switcher = not switcher
			row_str = Board.CLOSEDSPOT
			temp_str_2 = c_num_strip

			for i in range(self.width / 2):
				c_num += 1
				row_str += Board.EMPTY_SLOT + self.c_board[Board.num_c_positions + 1 - c_num] + Board.EMPTY_SLOT
				row_str += Board.CLOSEDSPOT

				if c_num < 10:
					temp_str_2 = temp_str_2.replace("XX", str(Board.num_c_positions+1-c_num), 1)
				else:
					temp_str_2 = temp_str_2.replace("XX", "0"+str(Board.num_c_positions+1-c_num), 1)

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