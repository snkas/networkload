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


def generate_from_to_reciprocated_random_pairing(servers, seed):

    # No duplicates in the servers array
    if len(set(servers)) != len(servers):
        raise ValueError("There are duplicate entries in the servers array: " + str(servers))
    if len(servers) < 2:
        raise ValueError("Cannot have less than two servers")
    if len(servers) % 2 != 0:
        raise ValueError("Must have an even amount of servers")
    servers = list(servers)

    # Set random seed
    random.seed(seed)

    # As long as possible to create a pair
    remaining = set(servers)
    from_to_tuples = []
    while len(remaining) != 0:
        chosen = random.sample(remaining, 2)
        from_to_tuples.append((chosen[0], chosen[1]))
        from_to_tuples.append((chosen[1], chosen[0]))
        remaining -= set(chosen)

    # Return from-to pairing
    return from_to_tuples
