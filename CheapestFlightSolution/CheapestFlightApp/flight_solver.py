from __future__ import annotations

import math
from typing import Iterable, List, Sequence, Tuple, Union


Flight = Tuple[int, int, int]
RawFlight = Union[Sequence[int], Sequence[float], dict]


class FlightSolver:
    """
    Compute the cheapest flight price within a maximum number of stops using Bellman-Ford.

    Bellman-Ford with a temporary array per iteration ensures we never exceed the allowed
    stop budget in a single relaxation pass.
    """

    def __init__(self, data: dict):
        self.n = int(data["n"])
        self.src = int(data["src"])
        self.dst = int(data["dst"])
        self.k = int(data["k"])
        self.flights: List[Flight] = self._normalize_flights(data["flights"])
        self._validate()

    def _validate(self) -> None:
        if self.n <= 0:
            raise ValueError("Number of cities must be positive")
        for name, value in (("src", self.src), ("dst", self.dst)):
            if not (0 <= value < self.n):
                raise ValueError(f"{name} index out of range for n={self.n}")
        if self.k < 0 and self.src != self.dst:
            raise ValueError("k must be non-negative unless src == dst")

    def _normalize_flights(self, raw_flights: Iterable[RawFlight]) -> List[Flight]:
        normalized: List[Flight] = []
        for flight in raw_flights:
            if isinstance(flight, dict):
                u, v, w = flight["from"], flight["to"], flight["price"]
            elif (
                isinstance(flight, (list, tuple))
                and len(flight) == 3
            ):
                u, v, w = flight
            else:
                raise ValueError(
                    "Flight must be a dict with keys 'from','to','price' "
                    "or a 3-item list/tuple like [from, to, price]"
                )
            u_i, v_i, w_i = int(u), int(v), float(w)
            if not (0 <= u_i < self.n and 0 <= v_i < self.n):
                raise ValueError(f"Invalid flight endpoints: {u_i}->{v_i} for n={self.n}")
            if w_i < 0:
                raise ValueError("Flight price must be non-negative")
            normalized.append((u_i, v_i, int(w_i)))
        return normalized

    def find_cheapest_price(self) -> int:
        if self.src == self.dst:
            return 0

        prices = [math.inf] * self.n
        prices[self.src] = 0

        # Relax edges exactly k+1 times (number of flights allowed is k+1)
        for _ in range(self.k + 1):
            next_prices = prices.copy()
            for u, v, w in self.flights:
                if prices[u] is math.inf:
                    continue
                cost = prices[u] + w
                if cost < next_prices[v]:
                    next_prices[v] = cost
            prices = next_prices

        return -1 if math.isinf(prices[self.dst]) else int(prices[self.dst])
