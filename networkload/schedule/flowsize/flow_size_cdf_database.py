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

# Filename: DCTCP_CDF
# Content:
# 0     1 0
# 10000 2 0.15
# 20000 3 0.2
# 30000 4 0.3
# 50000 5 0.4
# 80000 6 0.53
# 200000 7 0.6
# 1e+06 8 0.7
# 2e+06 9 0.8
# 5e+06 10 0.9
# 1e+07 11 0.97
# 3e+07 12 1
#
# Based on the Fig. 4 of DCTCP and Fig. 4(a) of pFabric,
# I estimate that origin CDF 0.0 should be 4000 bytes,
# as such that entry is edited to (4000, 0) instead of (0, 0).

CDF_PFABRIC_WEB_SEARCH_BYTE = [
    (4000, 0.0),
    (10000, 0.15),
    (20000, 0.2),
    (30000, 0.3),
    (50000, 0.4),
    (80000, 0.53),
    (200000, 0.6),
    (int(1e+06), 0.7),
    (int(2e+06), 0.8),
    (int(5e+06), 0.9),
    (int(1e+07), 0.97),
    (int(3e+07), 1.0),
]

# Filename: VL2_CDF
# Content:
# 0   1 0
# 180 2 0.1
# 216 3 0.2
# 560 4 0.3
# 900 5 0.4
# 1100 6 0.5
# 1870 7 0.6
# 3160 8 0.7
# 10000 9 0.8
# 400000 10 0.9
# 3.16e+06 11 0.95
# 1e+08 12 0.98
# 1e+09 13 1
#
# Based on the Fig. 2 of VL2 and Fig. 4(b) of pFabric,
# I estimate that origin CDF 0.0 should be 100 bytes,
# as such that entry is edited to (100, 0) instead of (0, 0).

CDF_PFABRIC_DATA_MINING_BYTE = [
    (100, 0.0),
    (180, 0.1),
    (216, 0.2),
    (560, 0.3),
    (900, 0.4),
    (1100, 0.5),
    (1870, 0.6),
    (3160, 0.7),
    (10000, 0.8),
    (400000, 0.9),
    (int(3.16e+06), 0.95),
    (int(1e+08), 0.98),
    (int(1e+09), 1.0)
]
