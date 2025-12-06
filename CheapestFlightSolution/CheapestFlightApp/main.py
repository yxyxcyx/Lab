from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from flight_solver import FlightSolver


def load_input(json_path: Path) -> dict:
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


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


def main() -> None:
    args = parse_args()
    data = load_input(args.input)
    solver = FlightSolver(data)
    price = solver.find_cheapest_price()
    print(price)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
