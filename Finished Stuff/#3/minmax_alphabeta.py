from board2 import *

def computer_move(board, depth):
	if board.game_over:
		return board
	if board.human_turn:
		raise ValueError("Computer attempted to move but was human's turn.")

	options = []
	board.generateChildren()
	for child in board.children:
		v = min_value(child, float("-inf"), float("inf"), depth-1)
		options.append([v, child])

	final_choice = max(options)
	best_value = max_value(board, float("-inf"), float("inf"), depth)

	return final_choice[1]

def max_value(board, alpha, beta, depth):
	if depth == 0:
		value = static_eval(board)
		return value

	board.generateChildren()
	for child in board.children:
		alpha = max(alpha, min_value(child, alpha, beta, depth-1))
		#print alpha
		if alpha >= beta:
			return alpha

	return alpha


def min_value(board, alpha, beta, depth):
	if depth == 0:
		value = static_eval(board)
		return value

	board.generateChildren()
	for child in board.children:
		beta = min(beta, max_value(child, alpha, beta, depth-1))
		#print beta
		if beta <= alpha:
			return beta

	return beta

def static_eval(board):
	num_edge_c_pieces = 0
	for c_piece in board.computer_positions:
		if c_piece in Board.edge_c_nums:
			num_edge_c_pieces += 1

	num_edge_h_pieces = 0
	for h_piece in board.human_positions:
		if h_piece in Board.edge_c_nums:
			num_edge_h_pieces += 1

	superior_pos = num_edge_c_pieces - num_edge_h_pieces

	num_c_pieces = len(board.computer_positions)
	num_h_pieces = len(board.human_positions)

	normal_pos = num_c_pieces - num_h_pieces # superior get counted a second time

	eval_value = superior_pos + normal_pos

	return eval_value