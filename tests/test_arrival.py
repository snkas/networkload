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
import random


class TestArrival(unittest.TestCase):

    def test_poisson_inter_arrival_gap(self):

        # Exponential distribution of inter-arrival gap
        random.seed(123456789)
        for arr_lambda in [(0.01, -1), (0.5, 1), (0.9, 1), (1.0, 2), (1.1, 1), (5, 2), (10, 2)]:
            drawn = []
            for i in range(100000):
                drawn.append(draw_poisson_inter_arrival_gap(arr_lambda[0]))
            self.assertAlmostEqual(float(np.mean(drawn)), 1.0 / arr_lambda[0], arr_lambda[1])
            self.assertAlmostEqual(float(np.median(drawn)), math.log(2) / arr_lambda[0], arr_lambda[1])
            self.assertAlmostEqual(
                float(np.std(drawn, ddof=1)),
                math.sqrt(1.0 / (arr_lambda[0] * arr_lambda[0])),
                arr_lambda[1]
            )

        # Poisson process as a whole
        random.seed(1234321)
        for arr in [(0.01, 1000000), (0.5, 20000), (0.9, 11111), (1.0, 10000), (1.1, 9999), (5, 2000), (100, 100),
                    (1000, 10)]:
            start_times = draw_poisson_inter_arrival_gap_start_times_ns(
                int(arr[1] * 1e9), arr[0], random.randint(0, 10000000)
            )

            # Mean arrival
            self.assertAlmostEqual(len(start_times), arr[0] * arr[1], delta=500)

            # Inter-arrival according to exponential distribution
            s = 0.0
            drawn = []
            for i in start_times:
                drawn.append((i - s) / 1e9)
                s = i
            self.assertAlmostEqual(float(np.mean(drawn)), 1.0 / arr[0], delta=((1.0 / arr[0]) / 25.0))
            self.assertAlmostEqual(float(np.median(drawn)), math.log(2) / arr[0], delta=((math.log(2) / arr[0]) / 25.0))
            self.assertAlmostEqual(
                float(np.std(drawn, ddof=1)),
                math.sqrt(1.0 / (arr[0] * arr[0])),
                delta=((math.sqrt(1.0 / (arr[0] * arr[0]))) / 25.0)
            )

        # Reproducibility
        self.assertEqual(
            draw_poisson_inter_arrival_gap_start_times_ns(int(10e9), 100, 12348558),
            draw_poisson_inter_arrival_gap_start_times_ns(int(10e9), 100, 12348558)
        )
        self.assertNotEqual(
            draw_poisson_inter_arrival_gap_start_times_ns(int(10e9), 100, 73728571),
            draw_poisson_inter_arrival_gap_start_times_ns(int(10e9), 100, 73728572)
        )

        # Poisson process checks
        random.seed(28958259)
        result = []
        for i in range(1000):
            result.append(
                len(draw_poisson_inter_arrival_gap_start_times_ns(int(1e9), 500, random.randint(0, 10000000)))
            )
        self.assertAlmostEqual(float(np.mean(result)), 500, delta=1.0)
        self.assertAlmostEqual(float(np.median(result)), math.floor(500 + 1/3 - 0.02/500.0), delta=1.0)
        self.assertAlmostEqual(float(np.std(result, ddof=1)), np.sqrt(500), delta=1.0)

    def test_constant_inter_arrival_gap(self):

        # Gaps
        for duration_ns in [300, 10 * 1000, 10 * 1000 * 1000, 30 * 1000 * 100 * 1000]:
            for arr_flows_per_s in [0.0001, 0.01, 0.5, 0.9, 1.0, 1.1, 5, 10]:
                start_times = draw_constant_inter_arrival_gap_start_times_ns(duration_ns, arr_flows_per_s)

                # Exact correctness
                s = 0.0
                exp_gap = 1.0 / arr_flows_per_s * 1e9
                for i in start_times:
                    s += exp_gap
                    self.assertEqual(int(round(s)), i)

                # Assert size of start_times
                self.assertTrue(len(start_times) >= int(math.floor(duration_ns / exp_gap)) - 2)

        # Reproducibility
        self.assertEqual(
            draw_constant_inter_arrival_gap_start_times_ns(int(10e9), 100),
            draw_constant_inter_arrival_gap_start_times_ns(int(10e9), 100)
        )
