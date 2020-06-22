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


class TestLeafSpineTopology(unittest.TestCase):

    def test_leaf_spine_valid(self):
        for dim in [(1, 1), (2, 3), (3, 3), (2, 2), (5, 5), (75, 33)]:
            num_leafs = dim[0]
            num_spines = dim[1]
            res = leaf_spine(num_leafs, num_spines)
            self.assertEqual(res.n, num_leafs + num_spines)
            self.assertEqual(res.switches, set(range(num_leafs + num_spines)))
            self.assertEqual(res.switches_which_are_tors, set(range(num_leafs)))
            self.assertEqual(res.servers, set())
            self.assertEqual(len(res.undirected_edges_set), len(set(res.undirected_edges_list)))
            self.assertEqual(res.undirected_edges_set, set(res.undirected_edges_list))
            self.assertEqual(len(res.undirected_edges_list), num_leafs * num_spines)
            not_tors = res.switches.difference(res.switches_which_are_tors)
            for i in res.switches_which_are_tors:
                self.assertEqual(res.adjacency_list[i], not_tors)
            for i in not_tors:
                self.assertEqual(res.adjacency_list[i], res.switches_which_are_tors)

    def test_leaf_spine_invalid(self):
        try:
            leaf_spine(0, 1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            leaf_spine(1, 0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            leaf_spine(1, -1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
