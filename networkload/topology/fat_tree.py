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

from .topology_type import *


def test_valid_k(k):
    if not (isinstance(k, int) and k % 2 == 0 and k > 1):
        raise ValueError("Invalid k=" + str(k) + ": must be integer and divisible by 2")


def edge_to_agg_links(k):
    """
    Generate the links between the edge and aggregation switches in each pod.
    Consists of k^3 links.

    :param k: k of the k-fat-tree (i.e., number of pods)

    :return: Edge-to-aggregation links
    """
    links = []
    for pod in range(k):
        for edge in range(int(k/2)):
            from_id = pod * int(k/2) + edge
            for agg in range(int(k/2)):
                to_id = int(k*k/2) + pod * int(k/2) + agg
                links.append((from_id, to_id))
    return links


def fat_tree_asymmetric(k):
    test_valid_k(k)

    # Connect edge to aggregation in each pod
    links = edge_to_agg_links(k)

    # Connect middle to core (total bi-directional edges added: k^3/4)
    for pod in range(k):  # Go over every pod
        for agg in range(int(k/2)):  # Each of the aggregation switches in the pod
            from_id = int(k*k/2) + pod * int(k/2) + agg
            for core in range(int(k/2)):  # Connects to k/2 cores (offset by agg * k/2 + pod)
                to_id = k*k + agg*int(k/2) + core + pod
                if to_id >= int(k*k*5/4):
                    to_id = to_id - int(k*k/4)
                links.append((from_id, to_id))

    return Topology(
        int(k*k*5/4),
        sorted(links),
        list(range(int(k*k*5/4))),
        list(range(int(k*k/2))),
        []
    )


def fat_tree_symmetric(k):
    test_valid_k(k)

    # Connect edge to aggregation in each pod
    links = edge_to_agg_links(k)

    # Connect middle to core (total bi-directional edges added: k^3/4)
    for pod in range(k):  # Go over every pod
        for agg in range(int(k/2)):  # Each of the aggregation switches in the pod
            from_id = int(k*k/2) + pod * int(k/2) + agg
            for core in range(int(k/2)):  # Connects to k/2 cores (offset by agg * k/2)
                to_id = k*k + agg * int(k/2) + core
                links.append((from_id, to_id))

    return Topology(
        int(k*k*5/4),
        sorted(links),
        list(range(int(k*k*5/4))),
        list(range(int(k*k/2))),
        []
    )
