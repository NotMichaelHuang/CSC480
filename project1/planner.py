import os
import argparse
from UCS import uniform_cost
from DFS import depth_first


"""
	_ - empty Cell
	# - Blocked Cell
	* - Dirty Cell
	@ - Robot Start Point
"""

def parse_cli():
	parser = argparse.ArgumentParser()

	# Aceepts either UCS or DFS
	parser.add_argument("algo", type=str, choices=["uniform-cost", "depth-first"], help="Search Algorithms: uniform-cost, depth-first")

	# .txt goes here
	parser.add_argument("map", type=str, help=".txt map path")

	args = parser.parse_args()

	if not args.map.endswith(".txt"):	
		raise ValueError("Map file extension must be .txt")

	if not os.path.isfile(args.map):
		raise FileNotFoundError(f"Map file not found: {args.map}")
	
	return args

def main():
	arguments = parse_cli()

	# Function dispatch
	dispatch = {
		"uniform-cost": uniform_cost,
		"depth-first": depth_first
	}
	dispatch[arguments.algo](arguments.map)
	return


if __name__ == "__main__":
	main()


