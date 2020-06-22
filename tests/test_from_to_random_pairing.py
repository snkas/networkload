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


def verify_from_to_reciprocated_random_pairing_checks(self, servers, seed):
    random.seed(seed)

    # Register how often a pair occurs
    pair_count = {}
    for i in servers:
        for j in servers:
            pair_count[(i, j)] = 0

    # Realize it many times
    num_realizations = 10000
    for i in range(num_realizations):
        from_to_list = generate_from_to_reciprocated_random_pairing(servers, random.randint(0, 10000000000))
        count = {}
        for j in servers:
            count[j] = 0
        for (a, b) in from_to_list:
            self.assertTrue((b, a) in from_to_list)
            count[a] += 1
            count[b] += 1
            pair_count[(a, b)] += 1
        for j in servers:
            self.assertEqual(count[j], 2)

    # Probability that a pair occurs is given that a is fixed, b is one of the other options, and this should
    # be equally likely for all of them even when we pick without replacement
    expectation_count = num_realizations * (1.0 / (len(servers) - 1))
    for i in servers:
        for j in servers:
            if i == j:
                self.assertEqual(pair_count[(i, j)], 0)
            else:
                self.assertTrue(pair_count[(i, j)] >= expectation_count * 0.8)


class TestFromToRandomPairing(unittest.TestCase):

    def test_reciprocated_random_pairing_correct(self):
        verify_from_to_reciprocated_random_pairing_checks(self, [0, 1, 2, 3], 64848848)
        verify_from_to_reciprocated_random_pairing_checks(self, [77, 66], 22525255)
        verify_from_to_reciprocated_random_pairing_checks(self, [55, 66, 11, 99], 22525255)
        verify_from_to_reciprocated_random_pairing_checks(self, list(range(0, 20)), 8928282758)
        verify_from_to_reciprocated_random_pairing_checks(self, list(range(547, 567)), 22255353)

    def test_reproducibility(self):
        res1 = generate_from_to_reciprocated_random_pairing(list(range(234, 466)), 4364266426)
        res2 = generate_from_to_reciprocated_random_pairing(list(range(236, 466)), 4364266426)
        res3 = generate_from_to_reciprocated_random_pairing(list(range(234, 466)), 547374372)
        res4 = generate_from_to_reciprocated_random_pairing(list(range(234, 466)), 4364266426)
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

    def test_from_to_reciprocated_random_pairing_fails(self):

        generate_from_to_reciprocated_random_pairing([0, 1], 123456789)

        # Less than two elements
        try:
            generate_from_to_reciprocated_random_pairing([0], 123456789)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Duplicates
        try:
            generate_from_to_reciprocated_random_pairing([1, 2, 1, 1], 123456789)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

        # Uneven
        try:
            generate_from_to_reciprocated_random_pairing([1, 2, 3, 4, 5], 123456789)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
