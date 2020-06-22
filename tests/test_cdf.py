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
import math


class TestCdf(unittest.TestCase):

    def test_draw_from_cdf_linear(self):
        random.seed(9892848)
        cdf = [
            (0, 0),
            (100, 0.5),
            (1000, 0.9),
            (10000, 1.0)
        ]
        drawn = []
        for i in range(100000):
            drawn.append(draw_from_cdf(cdf, linear_interpolate=True))
        self.assertAlmostEqual(float(np.median(drawn)), 100, -1)
        self.assertTrue(np.min(drawn) > 0.0)
        self.assertTrue(np.max(drawn) <= 10000)
        self.assertAlmostEqual(float(np.mean(drawn)), get_cdf_mean(cdf, linear_interpolate=True), -2)

    def test_draw_from_cdf_non_linear(self):
        random.seed(859338)
        cdf = [
            (0, 0),
            (100, 0.5),
            (1000, 0.9),
            (10000, 1.0)
        ]
        drawn = []
        for i in range(100000):
            drawn.append(draw_from_cdf(cdf, linear_interpolate=False))
        num_100 = 0
        num_1000 = 0
        num_10000 = 0
        for i in drawn:
            if i != 100 and i != 1000 and i != 10000:
                self.assertTrue(False)
            if i == 100:
                num_100 += 1
            elif i == 1000:
                num_1000 += 1
            elif i == 10000:
                num_10000 += 1
        self.assertTrue(np.min(drawn) >= 100)
        self.assertTrue(np.max(drawn) <= 10000)
        self.assertAlmostEqual(float(np.mean(drawn)), get_cdf_mean(cdf, linear_interpolate=False), -2)
        self.assertTrue(math.fabs(num_100 - 50000) < 500)
        self.assertTrue(math.fabs(num_1000 - 40000) < 500)
        self.assertTrue(math.fabs(num_10000 - 10000) < 500)

    def test_invalid_cdf(self):

        # Not starting at 0
        try:
            draw_from_cdf([(0, 0.01), (1000, 1.0)], linear_interpolate=True)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not ending at 1
        try:
            draw_from_cdf([(-100, 0.00), (1000, 0.999)], linear_interpolate=True)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not probability ascending
        try:
            draw_from_cdf([(0, 0.00), (100, 0.1), (400, 0.09), (1000, 1.0)], linear_interpolate=True)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not strictly probability ascending
        try:
            draw_from_cdf([(0, 0.00), (100, 0.1), (400, 0.1), (1000, 1.0)], linear_interpolate=True)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not value ascending
        try:
            draw_from_cdf([(0, 0.00), (100, 0.1), (90, 0.5), (1000, 1.0)], linear_interpolate=True)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Not even two values
        try:
            draw_from_cdf([(88, 1.00)], linear_interpolate=True)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
