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


def adjacency_matrix_to_undirected_edges_list(n, adjacency_matrix):
    undirected_edges = []
    if adjacency_matrix.shape != (n, n):
        raise ValueError("Invalid shape")
    for i in range(n):
        if adjacency_matrix[i, i] == 1:
            raise ValueError("Self-edges are not permitted")
        for j in range(i + 1, n):
            if adjacency_matrix[i, j] != adjacency_matrix[j, i]:
                raise ValueError("Graph is not bi-directional")
            elif adjacency_matrix[i, j] == 1:
                undirected_edges.append((i, j))
    return undirected_edges
