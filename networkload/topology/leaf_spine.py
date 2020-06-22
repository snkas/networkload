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


def leaf_spine(num_leafs, num_spines):
    """
    Generate a leaf-spine topology.

    :param num_leafs:   Number of leafs (ToRs)
    :param num_spines:  Number of spines

    :return: Topology
    """
    if num_leafs < 1 or num_spines < 1:
        raise ValueError("Number of leafs and spines must each be at least 1")

    links = []
    for leaf in range(num_leafs):
        from_id = leaf
        for spine in range(num_spines):
            to_id = num_leafs + spine
            links.append((from_id, to_id))

    return Topology(
        num_leafs + num_spines,
        sorted(links),
        list(range(num_leafs + num_spines)),
        list(range(num_leafs)),
        []
    )
