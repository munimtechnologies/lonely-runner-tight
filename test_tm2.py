# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Munim, Inc. (MV2, mv2@munimtech.com). Made with AI agents working in MV2's name.
"""Tests for tm2 (PREREG_q81.md, checks T1-T6). Standard library only."""
import math
import random
import unittest
from fractions import Fraction as Fr

import tm2


def dist(v, t):
    x = v * t - math.floor(v * t)
    return min(x, 1 - x)


class Checkers(unittest.TestCase):
    """T1: the two independent checkers on sets whose status is known."""

    def test_known_tight(self):
        for V, n in [([1, 2, 3, 4], 5), ([1, 3, 4, 7], 5), ([1, 3, 4, 5, 9], 6),
                     ([1, 2, 3, 4, 5, 6], 7), ([1, 2, 3, 4, 5, 6, 7], 8),
                     ([1, 2, 3, 4, 5, 7, 12], 8), ([1, 4, 5, 6, 7, 11, 13], 8),
                     ([2, 4, 6, 8], 5)]:
            self.assertTrue(tm2.is_cover(V, n), V)
            self.assertTrue(tm2.ml_at_least(V, n), V)

    def test_known_not_tight(self):
        # tight sets of 4..7 speeds are classified (Chen; Cordella; LeeMarshall1113, unrefereed)
        for V, n in [([1, 2, 3, 5], 5), ([1, 2, 4, 7], 5), ([1, 2, 3, 4, 6], 6),
                     ([1, 2, 3, 4, 5, 6, 8], 8)]:
            self.assertFalse(tm2.is_cover(V, n), V)

    def test_ml_brute(self):
        # ml_at_least against a dense exact grid on small random sets
        rng = random.Random(7)
        for _ in range(40):
            k = rng.randint(2, 4)
            V = sorted(rng.sample(range(1, 13), k))
            for n in (k + 1, k + 2):
                grid = any(all(n * dist(v, Fr(j, 4 * 3 * 5 * 7 * 11 * 13)) >= 1 for v in V)
                           for j in range(0, 4 * 3 * 5 * 7 * 11 * 13 // 2 + 1, 13))
                if grid:
                    self.assertTrue(tm2.ml_at_least(V, n), (V, n))


class GoddynWong(unittest.TestCase):
    """T2: the Theorem 5.1 matcher."""

    def test_thm51(self):
        self.assertTrue(tm2.is_thm51(8, [1, 2, 3, 4, 5, 7, 12]))
        self.assertTrue(tm2.is_thm51(8, list(range(1, 8))))
        self.assertFalse(tm2.is_thm51(8, [1, 4, 5, 6, 7, 11, 13]))
        V74 = [v for v in range(1, 74) if v not in (70, 72)] + [140, 144]
        self.assertTrue(tm2.is_thm51(74, V74))
        self.assertTrue(tm2.gw_criterion(74, 70, 2) and tm2.gw_criterion(74, 72, 2))
        self.assertFalse(tm2.gw_criterion(74, 70, 3))


class Sweep(unittest.TestCase):
    """T3: the uncovered pieces are exactly the points no speed of S covers."""

    def test_uncovered_exact(self):
        rng = random.Random(3)
        for n in range(6, 13):
            arcs = tm2.all_arcs(n)
            for r1 in range(1, n - 1):
                for r2 in range(r1 + 1, n):
                    S = [v for v in range(1, n) if v not in (r1, r2)]
                    U = tm2.uncovered(arcs, r1, r2)
                    for a, b in U:
                        mid = (a + b) / 2
                        self.assertTrue(all(n * dist(v, mid) > 1 for v in S))
                        self.assertTrue(any(n * dist(v, a) <= 1 for v in S))
                    for _ in range(30):
                        t = Fr(rng.randint(0, 10 ** 6), 2 * 10 ** 6)
                        inside = any(a < t < b or (t == b == tm2.HALF) for a, b in U)
                        covered = any(n * dist(v, t) <= 1 for v in S)
                        self.assertEqual(inside, not covered, (n, r1, r2, t))


class Census(unittest.TestCase):
    """T4-T6: the census against brute force and the known instances."""

    def test_small_census_matches_classification(self):
        # n = 5..8 (4..7 speeds, where tight sets are classified), every R, NO cap on the
        # inserted speeds: the tight two-entry modifications are the dilate {2,4,6,8} of
        # {1,2,3,4} at n = 5 and Goddyn-Wong's {1,4,5,6,7,11,13} at n = 8.
        done, note = tm2.run(5, 8, "all", workers=1)
        hits = sorted((n, tuple(h["R"]), tuple(h["W"])) for n in done for h in done[n]["hits"])
        self.assertEqual(hits, [(5, (1, 3), (6, 8)), (8, (2, 3), (11, 13))])
        dil = [h["dilate"] for n in done for h in done[n]["hits"]]
        self.assertEqual(sorted(dil), [False, True])
        for n in done:
            self.assertEqual(done[n]["anomalies"], [])
            self.assertEqual(done[n]["unresolved"], [])
            for h in done[n]["hits"]:
                self.assertTrue(h["cover"] and h["ml_ge"])

    def test_brute_force_agrees(self):
        for n in range(5, 9):
            done, _ = tm2.run(n, n, "all", workers=1)
            wmax = 6 * n
            census = sorted((n, tuple(h["R"]), tuple(h["W"])) for h in done[n]["hits"]
                            if max(h["W"]) <= wmax)
            self.assertEqual(sorted(tm2.brute(n, wmax)), census, n)

    def test_doubling_74(self):
        arcs = tm2.all_arcs(74)
        rec = tm2.classify_R(74, arcs, 70, 72)
        self.assertIn((140, 144), [tuple(h) for h in rec["hits"]])
        self.assertEqual(rec["anomalies"], [])


if __name__ == "__main__":
    unittest.main()
