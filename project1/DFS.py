from graph_handler import *


generated = 0
expanded = 0

def dfs(graph, goals, current, visited=None, path=None):
	global generated, expanded

	if visited is None:
		visited = set()
	if path is None:
		path = []		

	# Edge case
	if current in visited:
		return None	

	visited.add(current)
	path.append(current)	

	# Base case
	if current == goals:
		return path.copy()

	generated += len(graph.get(current, []))	
	for neighbors in graph.get(current, []):
		expanded += 1
		result = dfs(graph, goals, neighbors, visited, path)
		if result:
			return path

	path.pop() # Backtrack
	return None

def dfs_total_paths(graph, goals, start):
	current_state = start
	route = [start]
	for goal in goals:
		path = dfs(graph, goal, current_state)
		if not path:
			print(f"No path found from {current_state} to {goal}")
			return None	

		current_state = path[-1]
		route += path[1:]	

	return route

def depth_first(map_file: str):
	global generated, expanded
	map_list = []
	
	with open(map_file, "r") as file:
		map_list = [list(line.strip()) for line in file]

	grid_metadata = parse_list(map_list)
	grid = grid_metadata[2]
	
	valid = validate_grid(grid_metadata)
	if not valid:
		print("Error")
		
	start, goals = preprocess(grid)
	if start == (-1, -1):
		print("Error: Start position cannot be found")

	graph, _ = list_to_graph(grid_metadata)
	result = dfs_total_paths(graph, goals, start)
	card_path = coor_to_card(result, goals)
	card_path_with_nodes = attach_nodes(card_path, generated, expanded)
	output(card_path_with_nodes)

	return 0


