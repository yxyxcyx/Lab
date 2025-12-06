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

    # Test disconnected graph clusters: src and dst in completely separate subgraphs
    # Cluster A: nodes 0,1,2 fully connected. Cluster B: nodes 3,4,5 fully connected.
    # No edges between clusters. src=0 (in A), dst=5 (in B). Should return -1.
    def test_disconnected_clusters(self):
        data = {
            "n": 6,
            "flights": [
                # Cluster A: nodes 0, 1, 2
                [0, 1, 10],
                [1, 2, 10],
                [2, 0, 10],
                [0, 2, 15],
                # Cluster B: nodes 3, 4, 5
                [3, 4, 20],
                [4, 5, 20],
                [5, 3, 20],
                [3, 5, 25],
            ],
            "src": 0,
            "dst": 5,
            "k": 10,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), -1)

    # Test k equals n-1 (max possible stops, can visit every node)
    # Long cheap path vs short expensive path - large k allows finding cheaper route
    def test_max_stops_k_equals_n_minus_1(self):
        data = {
            "n": 5,
            "flights": [
                # Long cheap path: 0->1->2->3->4 = 10+10+10+10 = 40
                [0, 1, 10],
                [1, 2, 10],
                [2, 3, 10],
                [3, 4, 10],
                # Short expensive path: 0->4 = 100
                [0, 4, 100],
            ],
            "src": 0,
            "dst": 4,
            "k": 3,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 40)

    # Test tie-breaking: two paths with EXACT same cost but different stops
    # Path A: 0->1->3 = 50+50 = 100 (1 stop)
    # Path B: 0->2->1->3 = 30+20+50 = 100 (2 stops)
    # Both valid, algorithm should return 100 without crashing
    def test_tie_breaking_same_cost_different_stops(self):
        data = {
            "n": 4,
            "flights": [
                [0, 1, 50],
                [1, 3, 50],
                [0, 2, 30],
                [2, 1, 20],
            ],
            "src": 0,
            "dst": 3,
            "k": 2,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 100)

    # Sanity test: ensure algorithm picks strictly cheaper path with duplicate edges
    # Two edges from 0->1 with different costs, should use the cheaper one
    def test_strictly_cheaper_path_preferred(self):
        data = {
            "n": 3,
            "flights": [
                [0, 1, 100],
                [0, 1, 50],
                [1, 2, 10],
            ],
            "src": 0,
            "dst": 2,
            "k": 1,
        }
        solver = FlightSolver(data)
        self.assertEqual(solver.find_cheapest_price(), 60)


if __name__ == "__main__":
    unittest.main()
