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


def plus_grid(x, y):
    """
    Generate a +-grid topology.

    E.g., a x=3, y=3 example (it has 18 bi-directional edges):

       |    |    |
    -- 6 -- 7 -- 8 --
       |    |    |
    -- 3 -- 4 -- 5 --
       |    |    |
    -- 0 -- 1 -- 2 --
       |    |    |

    (Lower than 3 is not possible because if < 2 then edges to itself,
    if 2 then it would have two edges to its neighbors. In both cases it is
    not a simple graph, which it must be to be valid)

    :param x:   Number of nodes on the x-axis
    :param y:   Number of node on the y-axis

    :return: Topology
    """
    if x < 3 or y < 3:
        raise ValueError("Number of x and y must each be at least 3")

    links = []
    for i in range(x):
        for j in range(y):
            node_id = j * x + i
            links.append((node_id, j * x + ((i + 1) % x)))  # Right (bi-directional, so cannot add left explicitly)
            links.append((node_id, ((j + 1) % y) * x + i))  # Top (bi-directional, so cannot add bottom explicitly)

    return Topology(
            x * y,
            sorted(links),
            list(range(x * y)),
            list(range(x * y)),
            []
        )
