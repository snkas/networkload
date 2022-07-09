# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Code to draw from CDF and calculate mean.
# Based on: https://github.com/datacenter/empirical-traffic-gen/blob/master/src/ranvar.cpp (Giao Nguyen, Alizadeh et al)

import random


def draw_n_times_from_cdf(n, cdf, linear_interpolate, seed):
    random.seed(seed)
    res = []
    for i in range(n):
        res.append(draw_from_cdf(cdf, linear_interpolate))
    return res


def _validate_cdf(cdf):
    """
    Check that it is a valid CDF.
    Raises an exception iff the CDF is not valid.

    :param cdf:     Array of 2-tuples to represent CDF: e.g., [(val_0, 0), (val_1, 0.01), ..., (val_n-1, 1.0)]
    """

    # A CDF must consist of at least two points
    if len(cdf) < 2:
        raise ValueError("Invalid CDF: must have at least two points")

    prev = (-1, -1)
    for i in range(len(cdf)):

        # Validity of the CDF
        if i == 0 and cdf[i][1] != 0:
            raise ValueError("Invalid CDF: not starting at zero cumulative probability")
        if cdf[i][1] <= prev[1]:
            raise ValueError("Invalid CDF: not cumulative probability strictly ascending")
        if i == len(cdf) - 1 and cdf[i][1] != 1:
            raise ValueError("Invalid CDF: not ending at one cumulative probability")
        if cdf[i][0] < prev[0] and i != 0:
            raise ValueError("Invalid CDF: not value ascending")

        # Save previous to check for ascending
        prev = cdf[i]


def draw_from_cdf(cdf, linear_interpolate):
    """
    Draw from a cumulative distribution function (CDF).
    It uses random as random source, so be sure to set random.seed(...) beforehand for reproducibility.

    :param cdf:                     Array of 2-tuples to represent CDF:
                                    e.g., [(val_0, 0), (val_1, 0.01), ..., (val_n-1, 1.0)]
    :param linear_interpolate:      True iff there should be linear interpolation applied

    :return: Value drawn from the CDF
    """

    # CDF must be valid
    _validate_cdf(cdf)

    # Pick random number: 1 - [0, 1) = (0, 1]
    u = 1.0 - random.random()

    # Draw from CDF
    idx = -1
    for i in range(len(cdf)):

        # Actually finding the ceiling element
        if cdf[i][1] >= u:
            idx = i
            break

        # We should always find the element
        assert(i != len(cdf) - 1)

    # Linear interpolate if necessary
    if linear_interpolate and u < cdf[idx][1]:
        x1 = cdf[idx - 1][1]
        y1 = cdf[idx - 1][0]
        x2 = cdf[idx][1]
        y2 = cdf[idx][0]
        val = y1 + (u - x1) * (y2 - y1) / (x2 - x1)
    else:
        val = cdf[idx][0]

    return val


def get_cdf_mean(cdf, linear_interpolate):
    """
    Get the mean of the cumulative density function (CDF).

    :param cdf:                     Array of 2-tuples to represent CDF:
                                    e.g., [(val_0, 0), (val_1, 0.01), ..., (val_n-1, 1.0)]
    :param linear_interpolate:      True iff there should be linear interpolation applied

    :return: Expectation/mean value of the CDF
    """

    # CDF must be valid
    _validate_cdf(cdf)

    # Calculate average
    avg = 0.0
    for i in range(0, len(cdf)):
        if i > 0:
            if linear_interpolate:
                x1 = cdf[i - 1][1]
                y1 = cdf[i - 1][0]
                x2 = cdf[i][1]
                y2 = cdf[i][0]
                avg += (y1 + 0.5 * (y2 - y1)) * (x2 - x1)
            else:
                avg += (cdf[i][1] - cdf[i - 1][1]) * cdf[i][0]

    return avg
