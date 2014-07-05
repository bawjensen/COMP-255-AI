import Queue
from time import time

def BestFirstSearch(startingBoard):
	"""
	Search function incorporating the BestFS algorithm with a PriorityQueue and a visited list.
	"""

	q = Queue.PriorityQueue()
	q.put( (startingBoard.heuristic, startingBoard) )

	visited = [startingBoard]

	while not q.empty():
		qFront = q.get()
		newNode = qFront[1]


		if newNode.is_goal():
			answer = newNode.back_trace()
			return answer

		children = newNode.make_children()

		for newChild in children:
			if newChild not in visited:
				newChild.parent = newNode
				visited.append(newChild)
				q.put( (newChild.heuristic, newChild) )
				


def AStar(startingBoard):
	"""
	Search function incorporating the A* algorithm incorporating a PriorityQueue and an expanded list.
	"""

	q = Queue.PriorityQueue()
	q.put( (startingBoard.heuristic + startingBoard.steps, startingBoard) )

	expanded = []

	while not q.empty():

		qFront = q.get()
		newNode = qFront[1]

		if newNode.is_goal():
			answer = newNode.back_trace()
			return answer

		expanded.append(newNode)

		children = newNode.make_children()

		for newChild in children:
			# Checks to see if the child is already larger than the largest solution for a board (31)
			if newChild not in expanded and newChild.steps < 32:
				newChild.parent = newNode

				# Checks for newChild in queue
				foundNewChildNodeAt = [index for index, qSlot in enumerate(q.queue) if qSlot[1] == newChild]
				# If found:
				if type(foundNewChildNodeAt) == int:
					# Remove
					sameNode = q.queue.pop(foundNewChildNodeAt)
					# Re-heap the queue
					heapq.heapify(q.queue)
					# Put the smaller back on the queue
					if sameNode.steps < newChild.steps:
						q.put( (sameNode.heuristic + sameNode.steps, sameNode) )
					else:
						q.put( (newChild.heuristic + newChild.steps, newChild) )

				# If newChild isn't already on the queue, then just put it on.
				else:
					q.put( (newChild.heuristic + newChild.steps, newChild) )
