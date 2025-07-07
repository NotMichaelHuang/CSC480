
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

def list_to_graph(metadata: tuple) -> dict:
	cols, rows, grid = metadata
	graph = {}
	walkables = {"_", "*", "@"}
	up = (-1, 0)
	down = (1, 0)
	left = (0, -1)
	right = (0, 1)
	directions = [up, down, left, right]

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
	return graph


