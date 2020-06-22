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


class TestFlowSize(unittest.TestCase):

    def test_flow_size_constant(self):
        values = draw_n_times_constant_flow_size_byte(100, 10000)
        self.assertEqual([10000]*100, values)

    def test_cdf_drawing_reproducibility(self):
        for linear_interpolate in [False, True]:
            for cdf in [CDF_PFABRIC_WEB_SEARCH_BYTE, CDF_PFABRIC_DATA_MINING_BYTE]:
                res1 = draw_n_times_from_cdf(10000, cdf, linear_interpolate, 4364266426)
                res2 = draw_n_times_from_cdf(9999, cdf, linear_interpolate, 4364266426)
                res3 = draw_n_times_from_cdf(10000, cdf, linear_interpolate, 547374372)
                res4 = draw_n_times_from_cdf(10000, cdf, linear_interpolate, 4364266426)
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
