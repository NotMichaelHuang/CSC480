from grid_to_graph import *


def dfs(graph: dict, grid: list) -> any:
	pass

def depth_first(map_file: str):
	map_list = []
	
	with open(map_file, "r") as file:
		map_list = [list(line.strip()) for line in file]

	grid_metadata = parse_list(map_list)
	
	valid = validate_grid(grid_metadata)
	if not valid:
		print("Error")

	graph = list_to_graph(grid_metadata)
	dfs(graph, grid_metadata[2])
	print("Graph: ", graph)
	print("Grid: ", grid_metadata[2])
	return 0

