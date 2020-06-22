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

import random


def draw_n_times_from_to_all_to_all(n, servers, seed):

    # No duplicates in the servers array
    if len(set(servers)) != len(servers):
        raise ValueError("There are duplicate entries in the servers array: " + str(servers))
    if len(servers) < 2:
        raise ValueError("Cannot have less than two servers")
    servers = list(servers)

    # Set random seed
    random.seed(seed)

    # Draw n times
    from_to_tuples = []
    for i in range(n):
        src = random.randint(0, len(servers) - 1)
        dst = random.randint(0, len(servers) - 1)
        while src == dst:
            dst = random.randint(0, len(servers) - 1)
        from_to_tuples.append((servers[src], servers[dst]))

    return from_to_tuples
