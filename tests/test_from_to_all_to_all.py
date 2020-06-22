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
import numpy as np
import unittest


def verify_all_to_all_checks(other, n_draws, servers, seed):
    res = draw_n_times_from_to_all_to_all(n_draws, servers, seed)

    counters = {}
    for i in range(len(servers)):
        for j in range(len(servers)):
            if i != j:
                counters[(servers[i], servers[j])] = 0

    for val in res:
        other.assertTrue(val[0] in servers and val[1] in servers)
        other.assertNotEqual(val[0], val[1])
        counters[val] += 1

    for pair in counters:
        other.assertGreaterEqual(counters[pair], 10000 / (len(servers) * (len(servers) - 1)) * 0.95)

    # Model it as a uniform distribution
    draws_src = []
    draws_dst = []
    server_to_idx = {}
    for s in range(len(servers)):
        server_to_idx[servers[s]] = s
    for val in res:
        draws_src.append(server_to_idx[val[0]])
        draws_dst.append(server_to_idx[val[1]])

    # Variance check
    expected_variance = math.sqrt((math.pow(len(servers)-1 - 0 + 1, 2) - 1) / 12.0)
    other.assertAlmostEqual(
        float(np.std(draws_src, ddof=1)),
        expected_variance,
        delta=(0.01 * expected_variance)
    )
    other.assertAlmostEqual(
        float(np.std(draws_dst, ddof=1)),
        expected_variance,
        delta=(0.01 * expected_variance)
    )

    # Mean check
    expected_mean = (len(servers)-1 - 0) / 2.0
    other.assertAlmostEqual(
        float(np.mean(draws_src)),
        expected_mean,
        delta=(0.01 * expected_mean)
    )
    other.assertAlmostEqual(
        float(np.mean(draws_dst)),
        expected_mean,
        delta=(0.01 * expected_mean)
    )

    # Median check
    expected_median = (len(servers)-1 - 0) / 2.0
    other.assertAlmostEqual(
        float(np.mean(draws_src)),
        expected_median,
        delta=(0.01 * expected_median)
    )
    other.assertAlmostEqual(
        float(np.mean(draws_dst)),
        expected_median,
        delta=(0.01 * expected_median)
    )


class TestFromToAllToAll(unittest.TestCase):

    def test_all_to_all_correct(self):
        verify_all_to_all_checks(self, 70000, [0, 1, 2, 3], 4364266426)
        verify_all_to_all_checks(self, 70000, [0, 3, 6, 7], 2662626)
        verify_all_to_all_checks(self, 33333, [88, 9, 2], 1242352626)

    def test_reproducibility(self):
        res1 = draw_n_times_from_to_all_to_all(40000, [0, 8, 2, 3], 4364266426)
        res2 = draw_n_times_from_to_all_to_all(39999, [0, 8, 2, 3], 4364266426)
        res3 = draw_n_times_from_to_all_to_all(40000, [0, 8, 2, 3], 547374372)
        res4 = draw_n_times_from_to_all_to_all(40000, [0, 8, 2, 3], 4364266426)
        self.assertNotEqual(res1, res2)
        self.assertNotEqual(res1, res3)
        self.assertEqual(res1, res4)
        self.assertNotEqual(res2, res1)
        self.assertNotEqual(res2, res3)
        self.assertNotEqual(res2, res4)
        self.assertNotEqual(res3, res1)
        self.assertNotEqual(res3, res2)
        self.assertNotEqual(res3, res4)
        self.assertEqual(res4, res1)
        self.assertNotEqual(res4, res2)
        self.assertNotEqual(res4, res3)
        self.assertEqual(res1[0:len(res1)-1], res2)
        self.assertEqual(res4[0:len(res1)-1], res2)

    def test_all_to_all_fails(self):

        draw_n_times_from_to_all_to_all(40000, [0, 1], 123456789)

        # Less than two elements
        try:
            draw_n_times_from_to_all_to_all(40000, [0], 123456789)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Duplicates
        try:
            draw_n_times_from_to_all_to_all(40000, [1, 2, 1], 123456789)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
