from heapq import heapify, heappop, heappush
from graph_handler import *


generated = 0
expanded = 0

def sort_goals(goals, cost_map):
	return sorted(goals, key=lambda x: cost_map[x])		

def ucs(graph, goal, node, cost_map, visited=None, path=None):	
	global generated, expanded
	if visited is None:
		visited = set()
	if path is None:
		path = []

	# Cumulative cost, node, and path	
	frontier = [(0, node, [])]	
	heapify(frontier) # Create min-heap

	while frontier:
		cost, current_node, path = heappop(frontier)

		if current_node in visited:
			continue # Skip
		visited.add(current_node)
		path = path + [current_node]
		
		if current_node == goal:
			return path

		# Get it's edges
		expanded += len(graph.get(current_node, []))
		for neighbor in graph.get(current_node, []):	
			if neighbor not in visited:
				generated += 1
				weight = cost_map.get(neighbor, -1)
				# heapq is sorting/rebalancing by (cost + weight)
				heappush(frontier, (cost + weight, neighbor, path))

	return [] # No path...

def ucs_total_path(graph, goals, start, cost_map):
	current_state = start
	route = [start]
	goals = sort_goals(goals, cost_map)
	for goal in goals:
		path = ucs(graph, goal, current_state, cost_map)
		if not path:
			print(f"No path found from {current_state} to {goal}")
			return None
			
		current_state = path[-1]
		route += path[1:]

	return route

def uniform_cost(map_file: str):
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
	graph, cost_map = list_to_graph(grid_metadata, start, weighted=True)		

	result = ucs_total_path(graph, goals, start, cost_map)	
	card_path = coor_to_card(result, goals)
	card_path_with_nodes = attach_nodes(card_path, generated, expanded)
	output(card_path_with_nodes)
	
	return 0


