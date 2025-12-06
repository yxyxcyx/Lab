import unittest

from flight_solver import FlightSolver


class FlightSolverTests(unittest.TestCase):
    def test_happy_path(self):
        data = {
            "n": 4,
            "flights": [
                {"from": 0, "to": 1, "price": 100},
                {"from": 1, "to": 2, "price": 100},
                {"from": 2, "to": 3, "price": 100},
                {"from": 0, "to": 3, "price": 500},
            ],
            "src": 0,
            "dst": 3,
            "k": 2,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 300)

    def test_no_path_exists(self):
        data = {
            "n": 3,
            "flights": [
                {"from": 0, "to": 1, "price": 50},
            ],
            "src": 0,
            "dst": 2,
            "k": 1,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), -1)

    def test_path_exists_but_exceeds_k(self):
        data = {
            "n": 4,
            "flights": [
                {"from": 0, "to": 1, "price": 100},
                {"from": 1, "to": 2, "price": 100},
                {"from": 2, "to": 3, "price": 100},
            ],
            "src": 0,
            "dst": 3,
            "k": 1,  # need 2 stops (3 flights) but only 1 allowed
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), -1)

    def test_zero_stops_only_direct_allowed(self):
        data = {
            "n": 3,
            "flights": [
                {"from": 0, "to": 1, "price": 5},
                {"from": 1, "to": 2, "price": 5},
                {"from": 0, "to": 2, "price": 20},
            ],
            "src": 0,
            "dst": 2,
            "k": 0,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 20)

    def test_cycle_does_not_break(self):
        data = {
            "n": 3,
            "flights": [
                {"from": 0, "to": 1, "price": 1},
                {"from": 1, "to": 0, "price": 1},
                {"from": 1, "to": 2, "price": 10},
            ],
            "src": 0,
            "dst": 2,
            "k": 2,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 11)

    def test_input_validation_negative_n(self):
        data = {"n": -1, "flights": [], "src": 0, "dst": 0, "k": 0}
        with self.assertRaises(ValueError):
            FlightSolver(data)

    def test_accepts_list_flights(self):
        data = {
            "n": 3,
            "flights": [
                [0, 1, 5],
                [1, 2, 5],
            ],
            "src": 0,
            "dst": 2,
            "k": 1,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 10)


if __name__ == "__main__":
    unittest.main()
