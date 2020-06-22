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
import math


def draw_poisson_inter_arrival_gap(lambda_mean_arrival_rate):
    """
    Draw a poisson inter-arrival gap.
    It uses random as random source, so be sure to set random.seed(...) beforehand for reproducibility.

    E.g.:
    If lambda = 1000, then mean gap is 0.001
    If lambda = 0.1, then mean gap is 10

    :param lambda_mean_arrival_rate:     Lambda mean arrival rate (i.e., every 1 in ... an event arrives)

    :return: Value drawn from the exponential distribution (i.e., Poisson inter-arrival distribution)
    """
    return - math.log(1.0 - random.random(), math.e) / lambda_mean_arrival_rate


def draw_poisson_inter_arrival_gap_start_times_ns(duration_ns, lambda_mean_arrival_rate_flows_per_s, seed):
    random.seed(seed)
    start_times_ns = []
    s = 1e9 * draw_poisson_inter_arrival_gap(lambda_mean_arrival_rate_flows_per_s)
    while int(round(s)) < duration_ns:
        start_times_ns.append(int(round(s)))
        s += 1e9 * draw_poisson_inter_arrival_gap(lambda_mean_arrival_rate_flows_per_s)
    return start_times_ns
