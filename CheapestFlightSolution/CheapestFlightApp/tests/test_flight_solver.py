import unittest

from flight_solver import FlightSolver


class FlightSolverTests(unittest.TestCase):
    # Test basic functionality: finds the cheapest route (300) using 2 stops instead of direct flight (500)
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

    # Test when no route exists to destination: should return -1
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

    # Test when path exists but requires more stops than allowed: should return -1
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

    # Test k=0 means only direct flights allowed: must take direct (20) not cheaper via (10)
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

    # Test graph with cycles doesn't cause infinite loop or wrong answer
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

    # Test that negative number of cities raises ValueError
    def test_input_validation_negative_n(self):
        data = {"n": -1, "flights": [], "src": 0, "dst": 0, "k": 0}
        with self.assertRaises(ValueError):
            FlightSolver(data)

    # Test that flights can be provided as [from, to, price] list format (not just dict)
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

    # Test when source equals destination: should return 0 (no travel needed)
    def test_src_equals_dst(self):
        data = {
            "n": 3,
            "flights": [[0, 1, 100]],
            "src": 0,
            "dst": 0,
            "k": 1,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 0)

    # Test that negative flight prices raise ValueError (prices must be >= 0)
    def test_negative_price_raises_error(self):
        data = {
            "n": 3,
            "flights": [[0, 1, -100]],
            "src": 0,
            "dst": 2,
            "k": 1,
        }
        with self.assertRaisesRegex(ValueError, "Flight price must be non-negative"):
            FlightSolver(data)

    # Test that flight referencing non-existent city (index >= n) raises ValueError
    def test_invalid_city_index(self):
        data = {
            "n": 3,
            "flights": [[0, 5, 100]],
            "src": 0,
            "dst": 2,
            "k": 1,
        }
        with self.assertRaisesRegex(ValueError, "Invalid flight endpoints"):
            FlightSolver(data)

    # Test that negative k (max stops) raises ValueError
    def test_negative_k_raises_error(self):
        data = {
            "n": 3,
            "flights": [[0, 1, 100]],
            "src": 0,
            "dst": 1,
            "k": -2,
        }
        with self.assertRaisesRegex(ValueError, "k must be non-negative"):
            FlightSolver(data)

    # Test malformed flight data: wrong list length or missing dict keys raises error
    def test_malformed_flight_data(self):
        # Case 1: List with only 2 elements
        data_short_list = {
            "n": 3, "flights": [[0, 1]], "src": 0, "dst": 2, "k": 1
        }
        with self.assertRaisesRegex(ValueError, "Flight must be a dict"):
            FlightSolver(data_short_list)

        # Case 2: Dict missing 'price'
        data_bad_dict = {
            "n": 3,
            "flights": [{"from": 0, "to": 1}],
            "src": 0, "dst": 2, "k": 1
        }
        with self.assertRaises(KeyError):
            FlightSolver(data_bad_dict)

    # Test empty flights list: should return -1 when src != dst (no way to travel)
    def test_empty_flights_list(self):
        data = {
            "n": 3,
            "flights": [],
            "src": 0,
            "dst": 2,
            "k": 1,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), -1)


if __name__ == "__main__":
    unittest.main()
