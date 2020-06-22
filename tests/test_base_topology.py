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
import numpy as np


class TestBaseTopology(unittest.TestCase):

    def test_construction_valid(self):
        plus_grid(11, 3)
        leaf_spine(6, 7)
        fat_tree_asymmetric(6)
        fat_tree_symmetric(4)
        extend_tors_with_servers(plus_grid(11, 3), 2)
        extend_tors_with_servers(leaf_spine(5, 5), 3)
        extend_tors_with_servers(fat_tree_asymmetric(6), 1)
        extend_tors_with_servers(fat_tree_symmetric(4), 70)

    def test_str(self):
        self.assertEqual(
            str(extend_tors_with_servers(leaf_spine(5, 7), 11)),
            "Topology(#nodes=67 (12 switches (of which 5 are ToRs), 55 servers), #edges=90)"
        )

    def test_construction_invalid(self):
        Topology(
            4,
            [(0, 1), (1, 2), (1, 3)],
            [0, 1, 2],
            [1],
            [3]
        )

        # Duplicate edge I
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3), (1, 3)],
                [0, 1, 2],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Duplicate edge II
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3), (2, 1)],
                [0, 1, 2],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Invalid endpoints I
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 4)],
                [0, 1, 2],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Invalid endpoints II
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (-1, 3)],
                [0, 1, 2],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Duplicate switches
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2, 1],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Duplicate switches which are ToRs
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2],
                [1, 1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Duplicate servers
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2],
                [1],
                [3, 3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not valid switch id
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2, -1],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not valid ToR id
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2],
                [1, -5],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not valid server id
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2],
                [1],
                [3, -1]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Servers and switches not distinct
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2],
                [1],
                [3, 0]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Servers and switches do not cover all nodes
        try:
            Topology(
                5,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Server is a ToR
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3)],
                [0, 1, 2],
                [1, 3],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Server is connected to two ToRs
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (1, 3), (3, 0)],
                [0, 1, 2],
                [0, 1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Server edge to non-ToR
        try:
            Topology(
                4,
                [(0, 1), (1, 2), (3, 0)],
                [0, 1, 2],
                [1],
                [3]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Server edge to non-ToR
        try:
            Topology(
                4,
                [(1, 2), (2, 3), (0, 3)],
                [1, 2, 3],
                [2],
                [0]
            )
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_matrix_to_list(self):

        # Good matrix
        a = np.zeros((3, 3))
        a[0][1] = 1
        a[1][0] = 1
        self.assertEqual([(0, 1)], adjacency_matrix_to_undirected_edges_list(3, a))

        # Not bi-directional
        try:
            a = np.zeros((3, 3))
            a[0][1] = 1
            adjacency_matrix_to_undirected_edges_list(3, a)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Self-edge
        try:
            a = np.zeros((3, 3))
            a[1][1] = 1
            adjacency_matrix_to_undirected_edges_list(3, a)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Wrong shape
        try:
            a = np.zeros((3, 3))
            a[0][1] = 1
            a[1][0] = 1
            adjacency_matrix_to_undirected_edges_list(4, a)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
