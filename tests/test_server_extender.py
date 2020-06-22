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


class TestServerExtender(unittest.TestCase):

    def test_extending_success(self):
        for original in [leaf_spine(4, 4), fat_tree_symmetric(6), fat_tree_asymmetric(4), plus_grid(9, 16)]:
            for num_servers_per_tor in [1, 3, 20]:
                extended = extend_tors_with_servers(original, num_servers_per_tor)
                self.assertEqual(original.n + num_servers_per_tor * len(extended.switches_which_are_tors), extended.n)
                self.assertEqual(original.switches, extended.switches)
                self.assertEqual(original.switches_which_are_tors, extended.switches_which_are_tors)
                self.assertTrue(original.undirected_edges_set.issubset(extended.undirected_edges_set))
                for not_tor in extended.switches.difference(extended.switches_which_are_tors):
                    self.assertEqual(original.adjacency_list[not_tor], extended.adjacency_list[not_tor])
                all_servers = []
                for tor in extended.switches_which_are_tors:
                    self.assertTrue(original.adjacency_list[tor].issubset(extended.adjacency_list[tor]))
                    for j in extended.adjacency_list[tor].difference(original.adjacency_list[tor]):
                        self.assertTrue(j in extended.servers)
                        all_servers.append(j)
                    self.assertEqual(
                        len(original.adjacency_list[tor]) + num_servers_per_tor,
                        len(extended.adjacency_list[tor])
                    )
                self.assertEqual(len(all_servers), len(set(all_servers)))
                self.assertEqual(extended.servers, set(all_servers))

    def test_extending_failure(self):
        extend_tors_with_servers(leaf_spine(3, 4), 2)

        # Zero extending servers
        try:
            extend_tors_with_servers(leaf_spine(3, 4), 0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Already servers
        try:
            extend_tors_with_servers(extend_tors_with_servers(leaf_spine(3, 4), 2), 2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
