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


def verify_fat_tree_invariant(other, k, res):
    other.assertEqual(res.n, k * k * 5 / 4)
    other.assertEqual(res.switches, set(range(int(k * k * 5 / 4))))
    other.assertEqual(res.switches_which_are_tors, set(range(int(k * k / 2))))
    other.assertEqual(res.servers, set())
    other.assertEqual(len(res.undirected_edges_set), len(set(res.undirected_edges_list)))
    other.assertEqual(res.undirected_edges_set, set(res.undirected_edges_list))
    other.assertEqual(len(res.undirected_edges_list), int(k * k * k / 2))

    # Edge links
    for edge in range(0, int(k * k / 2)):
        pod = int(math.floor(edge / (k / 2)))
        other.assertEqual(res.adjacency_list[edge], set(range(int(k*k/2 + pod * (k/2)), int(k*k/2 + (pod + 1) * k/2))))

    # Check each pod
    for pod in range(int(k/2)):

        pod_neighbors = set()
        for agg in range(int(k*k/2 + pod * k/2), int(k*k/2 + (pod + 1) * k/2)):

            # Each agg must have a link to all edge ToRs in its pod
            other.assertTrue(set(range(int(pod * (k/2)), int((pod + 1) * k/2))).issubset(res.adjacency_list[agg]))

            # Each agg must have exactly k edges
            other.assertEqual(len(res.adjacency_list[agg]), k)

            # Neighboring cores
            neighboring_cores = res.adjacency_list[agg].difference(set(range(int(pod * (k/2)), int((pod + 1) * k/2))))
            other.assertEqual(len(neighboring_cores), k/2)

            # The other edges must be to the core
            other.assertTrue(
                neighboring_cores.issubset(set(range(int(k*k), int(k*k*5/4))))
            )

            # Add the cores this aggregation node connects to to the pod's neighbors
            pod_neighbors = pod_neighbors.union(neighboring_cores)

        # The pod must exactly connect to all cores
        other.assertEqual(pod_neighbors, set(range(int(k*k), int(k*k*5/4))))

    # Check each core
    for core in range(int(k*k), int(k*k*5/4)):
        other.assertEqual(len(res.adjacency_list[core]), k)
        pod_counter = [0]*k
        for agg in res.adjacency_list[core]:
            pod_counter[int(math.floor((agg - k*k/2) / (k/2)))] += 1
        for i in pod_counter:
            other.assertEqual(i, 1)


class TestFatTreeTopology(unittest.TestCase):

    def test_fat_tree_symmetric_valid(self):
        for k in [2, 4, 8, 10, 34]:
            res = fat_tree_symmetric(k)
            verify_fat_tree_invariant(self, k, res)

            # Agg links
            for agg in range(int(k * k / 2), int(k * k)):
                pod = int(math.floor((agg - k*k/2) / (k / 2)))
                core_start_idx = (agg % (int(k/2))) * k/2
                self.assertEqual(
                    res.adjacency_list[agg],
                    set(range(int(pod * (k/2)), int((pod + 1) * k/2))).union(
                        set(range(int(k*k + core_start_idx), int(k*k + core_start_idx + k/2)))
                    )
                )

            # Core links
            for core in range(int(k*k), int(k*k*5/4)):
                core_idx = core - k*k
                agg_idx = int(math.floor(core_idx / (k/2)))
                self.assertEqual(res.adjacency_list[core], set(range(int(k*k/2 + agg_idx), int(k*k), int(k/2))))

    def test_fat_tree_asymmetric_valid(self):
        for k in [2, 4, 8, 10, 34]:
            res = fat_tree_asymmetric(k)
            verify_fat_tree_invariant(self, k, res)

            # Agg links
            for agg in range(int(k * k / 2), int(k * k)):
                pod = int(math.floor((agg - k*k/2) / (k / 2)))
                core_start_idx = (agg % (int(k/2))) * k/2 + pod
                self.assertEqual(
                    res.adjacency_list[agg],
                    set(range(int(pod * (k/2)), int((pod + 1) * k/2))).union(
                        set(k*k + (x % (k*k/4)) for x in set(range(int(core_start_idx), int(core_start_idx + k/2))))
                    )
                )

            # Core links
            for core in range(int(k*k), int(k*k*5/4)):
                core_idx = core - k*k
                must_be_connected = set()
                for pod in range(k):
                    must_be_connected.add(int(
                        k*k/2 + pod * k/2 + int(math.floor((core_idx - pod) / (k/2)) + (k/2)) % int(k/2))
                    )
                self.assertEqual(len(must_be_connected), k)
                self.assertEqual(res.adjacency_list[core], must_be_connected)

    def test_fat_tree_invalid(self):
        try:
            fat_tree_asymmetric(1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            fat_tree_symmetric(-2)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
        try:
            fat_tree_symmetric(0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)
