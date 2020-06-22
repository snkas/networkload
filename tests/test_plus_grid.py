# The MIT License (MIT)
#
# Copyright (c) snkas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from networkload import *
import unittest


def verify_plus_grid_basic_invariants(self, res, x, y):
    self.assertEqual(res.n, x * y)
    self.assertEqual(res.switches, set(range(x * y)))
    self.assertEqual(res.switches_which_are_tors, set(range(x * y)))
    self.assertEqual(res.servers, set())
    self.assertEqual(len(res.undirected_edges_set), len(set(res.undirected_edges_list)))
    self.assertEqual(res.undirected_edges_set, set(res.undirected_edges_list))
    self.assertEqual(len(res.undirected_edges_list), 4 * x * y / 2)
    for idx in res.switches:
        self.assertEqual(len(res.adjacency_list[idx]), 4)
        i = idx % x
        j = int(math.floor(idx / x))
        self.assertEqual(res.adjacency_list[idx],
                         {
                             j * x + (i - 1 + x) % x,
                             j * x + (i + 1 + x) % x,
                             ((j - 1 + y) % y) * x + i,
                             ((j + 1 + y) % y) * x + i
                         }
                         )


class TestPlusGridTopology(unittest.TestCase):

    def test_plus_grid_valid_manual(self):
        res = plus_grid(3, 4)
        self.assertEqual(
            res.undirected_edges_set,
            {
                (0, 1),
                (0, 3),
                (1, 2),
                (1, 4),
                (0, 2),
                (2, 5),
                (3, 6),
                (3, 4),
                (4, 5),
                (4, 7),
                (3, 5),
                (5, 8),
                (6, 7),
                (6, 9),
                (7, 8),
                (7, 10),
                (6, 8),
                (8, 11),
                (9, 10),
                (0, 9),
                (10, 11),
                (1, 10),
                (9, 11),
                (2, 11)
            }
        )

    def test_plus_grid_valid(self):
        for dim in [(3, 3), (3, 4), (4, 3), (5, 4), (4, 5), (4, 4), (5, 7), (89, 89)]:
            x = dim[0]
            y = dim[1]
            res = plus_grid(x, y)
            verify_plus_grid_basic_invariants(self, res, x, y)

    def test_plus_grid_invalid(self):
        try:
            plus_grid(0, 1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            plus_grid(1, 0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            plus_grid(1, -1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            plus_grid(1, 2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            plus_grid(2, 1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            plus_grid(3, 2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            plus_grid(2, 3)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
