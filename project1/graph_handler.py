from collections import deque


def card_directions() -> list[tuple]:
	up = (-1, 0)
	down = (1, 0)
	left = (0, -1)
	right = (0, 1)
	directions = [up, down, left, right]
	return directions

def parse_list(map_data: list) -> tuple:
	# cols, rows, grid
	return (int(map_data[0][0]), int(map_data[1][0]), map_data[2:])

def validate_grid(metadata: tuple) -> bool:	
	cols, rows, grid = metadata
	if rows != len(grid):
		print("Rows does not match")
		return False

	for i, row in enumerate(grid):
		if len(row) != cols:
			print(f"Columns mismatch: Row {i}\nExpected {cols}\nYield {len(row)}")
			return False
	return True	

# BFS
def compute_cost(node, graph):	
	visited = set()

	visited.add(node)
	queue = deque([(node, 0)])
	cost = {node: 0}
	
	while queue:
		current_node, current_cost = queue.popleft()
		for neighbor in graph.get(current_node, []):
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append((neighbor, current_cost + 1))
				cost[neighbor] = current_cost + 1	

	return cost	

def list_to_graph(metadata: tuple, start=None, weighted=False):
	cols, rows, grid = metadata
	cost = {}
	graph = {}
	walkables = {"_", "*", "@"}	
	directions = card_directions()

	for row in range(rows):
		for col in range(cols):
			if grid[row][col] not in walkables:
					continue # Skip walls or out-of-bound

			current_node = (row, col)
			neighbors = []

			# Tuple unpacking
			for direction_row, direction_col in directions:	
				new_row, new_col = row + direction_row, col + direction_col
				# Prevent coordinates off the grid
				if 0 <= new_row < rows and 0 <= new_col < cols:
					# Block cell?
					if grid[new_row][new_col] in walkables:
						neighbors.append((new_row, new_col))	

			graph[current_node] = neighbors

	if weighted:
		cost = compute_cost(start, graph)

	return (graph, cost)

def preprocess(grid: list[list]) -> (tuple, list[tuple]):
	start = None
	goals = []
	for i, row in enumerate(grid): # Rows
		for j, col in enumerate(row): # Columns
			if col == "@":
				start = (i, j)
			elif col == "*":
				goals.append((i, j))
	return (start, goals)

def coor_to_card(route: list[tuple], goals: list[tuple]) -> list[str]:
	card_path = []
	c_row, c_col = route[0]
	path = route[1:]

	directions = card_directions()
	cardinal_direaction = {directions[0]: "N", directions[1]: "S", 
												directions[2]: "W", directions[3]: "E"}

	for row, col in path:	
		new_row, new_col = row - c_row, col - c_col	
		c_row, c_col = row, col	

		card_path.append(cardinal_direaction.get((new_row, new_col)))
		if (row, col) in goals:
			goals.remove((row, col))
			card_path.append("V")			

	return card_path

def attach_nodes(path, gen: int, exp: int) -> list[str]:
	path.append(str(gen) + " nodes generated")
	path.append(str(exp) + " nodes expanded")
	return path

def output(path) -> None:
	for item in path:
		print(item)



