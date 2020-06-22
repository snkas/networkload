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


class TestScheduleWriter(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("temp.txt"):
            os.remove("temp.txt")

    def test_valid_one(self):
        write_schedule(
            "temp.txt",
            1,
            [(8, 1)],
            [8],
            [999],
            list_metadata=["a"]
        )
        with open("temp.txt", "r") as f_in:
            lines = []
            for line in f_in:
                lines.append(line)
            self.assertEqual(lines[0].strip(), "0,8,1,8,999,,a")
            self.assertEqual(len(lines), 1)

    def test_valid_multiple(self):
        write_schedule(
            "temp.txt",
            5,
            [(0, 1), (1, 2), (4, 5), (3, 4), (99, 2)],
            [3395, 200, 3949, 111, 222],
            [1000, 1000, 1000, 9999, 9],
            ["a", "", "", "", "x=g;d=f"],
            ["a", "a", "b", "", "d"]
        )
        with open("temp.txt", "r") as f_in:
            lines = []
            for line in f_in:
                lines.append(line)
            self.assertEqual(lines[0].strip(), "0,0,1,3395,1000,a,a")
            self.assertEqual(lines[1].strip(), "1,1,2,200,1000,,a")
            self.assertEqual(lines[2].strip(), "2,4,5,3949,1000,,b")
            self.assertEqual(lines[3].strip(), "3,3,4,111,9999,,")
            self.assertEqual(lines[4].strip(), "4,99,2,222,9,x=g;d=f,d")
            self.assertEqual(len(lines), 5)

    def test_invalid_sizes(self):

        list_pairs = [(0, 1), (1, 2), (4, 5), (3, 4), (99, 2)]
        list_start_times = [3395, 200, 3949, 111, 222]
        list_flow_sizes = [1000, 1000, 1000, 9999, 9]
        list_extra_parameters = ["a", "", "", "", "x=g;d=f"]
        list_metadata = ["a", "a", "b", "", "d"]

        write_schedule("temp.txt", 5, list_pairs, list_start_times, list_flow_sizes)

        # Zero
        try:
            write_schedule("temp.txt", 0, [], [], [])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Pairs
        try:
            write_schedule("temp.txt", 5, list_pairs[0:4], list_start_times, list_flow_sizes)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Start times
        try:
            write_schedule("temp.txt", 5, list_pairs, list_start_times[0:4], list_flow_sizes)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Flow sizes
        try:
            write_schedule("temp.txt", 5, list_pairs, list_start_times, list_flow_sizes[0:4])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Extra parameters
        try:
            write_schedule("temp.txt", 5, list_pairs, list_start_times, list_flow_sizes, list_extra_parameters[0:4])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Metadata
        try:
            write_schedule("temp.txt", 5, list_pairs, list_start_times, list_flow_sizes,
                           list_metadata=list_metadata[0:4])
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
