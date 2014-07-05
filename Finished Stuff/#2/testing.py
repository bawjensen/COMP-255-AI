board = [ [3, 1, 2], [4, 7, 5], [6, 8, 0] ]

for row in range(len(board)):
	try:
		frank = board[row].index(0)
		jill = row
	except:
		pass

print frank, jill