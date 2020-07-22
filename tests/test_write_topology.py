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
import os


class TestBaseTopology(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("temp_topology.properties"):
            os.remove("temp_topology.properties")

    def test_topology_writer_valid(self):
        write_topology(
            "temp_topology.properties",
            Topology(
                6,
                [(0, 1), (1, 2), (0, 4), (2, 3), (5, 1)],
                [0, 1, 2, 5],
                [0, 2],
                [3, 4]
            )
        )
        with open("temp_topology.properties", "r") as f_in:
            lines = []
            for line in f_in:
                lines.append(line)
            self.assertEqual(lines[0].strip(), "num_nodes=6")
            self.assertEqual(lines[1].strip(), "num_undirected_edges=5")
            self.assertEqual(lines[2].strip(), "switches=set(0,1,2,5)")
            self.assertEqual(lines[3].strip(), "switches_which_are_tors=set(0,2)")
            self.assertEqual(lines[4].strip(), "servers=set(3,4)")
            self.assertEqual(lines[5].strip(), "undirected_edges=set(0-1,0-4,1-2,1-5,2-3)")
            self.assertEqual(len(lines), 6)

    def test_topology_writer_valid_reordered(self):
        write_topology(
            "temp_topology.properties",
            Topology(
                6,
                [(1, 2), (0, 1), (0, 4), (2, 3), (5, 1)],
                [0, 2, 1, 5],
                [2, 0],
                [4, 3]
            )
        )
        with open("temp_topology.properties", "r") as f_in:
            lines = []
            for line in f_in:
                lines.append(line)
            self.assertEqual(lines[0].strip(), "num_nodes=6")
            self.assertEqual(lines[1].strip(), "num_undirected_edges=5")
            self.assertEqual(lines[2].strip(), "switches=set(0,1,2,5)")
            self.assertEqual(lines[3].strip(), "switches_which_are_tors=set(0,2)")
            self.assertEqual(lines[4].strip(), "servers=set(3,4)")
            self.assertEqual(lines[5].strip(), "undirected_edges=set(0-1,0-4,1-2,1-5,2-3)")
            self.assertEqual(len(lines), 6)
