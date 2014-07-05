from board2 import *
from minmax_alphabeta import *

def main():
	b = Board(width=6, humanFirst=True)
	b.initialize_board(num_pieces=4)

	while not b.game_over:
		while True:
			print b
			start, end = "", ""
			try:
				start, end = raw_input("Enter move: ").split(" ")
				if start.lower() == "z" or end.lower() == "z":
					return
				start, end = int(start), int(end)

				if b.movePiece(start, end):
					break
				else:
					raise ValueError("Invalid move.")
			except:
				print "Possible moves: %s." %[[move for move in b.moves_by_c_num[c_num]] for c_num in b.human_positions]
				print "Try again...\n"
		
		print "HUMAN Move:"
		print b
		print "COMPUTER MOVE:"
		b = computer_move(b, depth=1)

	print b
	print "GAME OVER."
	if not b.human_positions:
		print "You lose..."
	else:
		print "You win :)"

if __name__ == "__main__":
	main()