from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import List, Tuple

from flight_solver import FlightSolver


# Load input data from a JSON file
def load_input(json_path: Path) -> dict:
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


# Parse command line arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute the cheapest flight within K stops using Bellman-Ford."
    )
    default_path = Path(os.path.dirname(__file__)) / "data" / "input.json"
    parser.add_argument(
        "--input",
        type=Path,
        default=default_path,
        help=f"Path to input JSON (default: {default_path})",
    )
    return parser.parse_args()


# Print a formatted header
def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


# Display the problem parameters
def print_problem_info(data: dict) -> None:
    print_header("PROBLEM PARAMETERS")
    print(f"  Number of cities (n): {data['n']}")
    print(f"  Source city:          {data['src']}")
    print(f"  Destination city:     {data['dst']}")
    print(f"  Max stops allowed (k): {data['k']}")


# Display the flight graph in a readable format
def print_graph(data: dict) -> None:
    print_header("FLIGHT GRAPH")
    
    n = data["n"]
    flights = data["flights"]
    
    # Build adjacency list for display
    adj: dict = {i: [] for i in range(n)}
    for flight in flights:
        if isinstance(flight, dict):
            u, v, w = flight["from"], flight["to"], flight["price"]
        else:
            u, v, w = flight[0], flight[1], flight[2]
        adj[u].append((v, w))
    
    # Print each city and its outgoing flights
    print("\n  [City] --> [Destination: Cost]")
    print("  " + "-" * 40)
    
    for city in range(n):
        if adj[city]:
            destinations = ", ".join([f"{v}: ${w}" for v, w in adj[city]])
            marker = ""
            if city == data["src"]:
                marker = " (SOURCE)"
            elif city == data["dst"]:
                marker = " (DEST)"
            print(f"  City {city}{marker} --> {destinations}")
        else:
            marker = ""
            if city == data["src"]:
                marker = " (SOURCE)"
            elif city == data["dst"]:
                marker = " (DEST)"
            print(f"  City {city}{marker} --> (no outgoing flights)")
    
    # Print visual representation
    print("\n  Visual Graph:")
    print("  " + "-" * 40)
    for city in range(n):
        for dest, cost in adj[city]:
            src_label = f"[{city}]"
            dst_label = f"[{dest}]"
            if city == data["src"]:
                src_label = f"[{city}:SRC]"
            if city == data["dst"]:
                src_label = f"[{city}:DST]"
            if dest == data["src"]:
                dst_label = f"[{dest}:SRC]"
            if dest == data["dst"]:
                dst_label = f"[{dest}:DST]"
            print(f"  {src_label} --${cost}--> {dst_label}")


# Display the result in a formatted way
def print_result(price: int, src: int, dst: int, k: int) -> None:
    print_header("RESULT")
    
    if price == -1:
        print(f"\n  No valid route found from City {src} to City {dst}")
        print(f"  within {k} stop(s).")
        print("\n  Result: -1 (unreachable)")
    else:
        print(f"\n  Cheapest flight from City {src} to City {dst}")
        print(f"  with at most {k} stop(s):")
        print(f"\n  --> Total Cost: ${price}")
    
    print("\n" + "=" * 60)


# Main entry point
def main() -> None:
    args = parse_args()
    data = load_input(args.input)
    
    # Display problem info and graph
    print_problem_info(data)
    print_graph(data)
    
    # Solve and display result
    solver = FlightSolver(data)
    price = solver.find_cheapest_price()
    print_result(price, data["src"], data["dst"], data["k"])
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
