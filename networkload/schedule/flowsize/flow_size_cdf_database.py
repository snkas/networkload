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

# Based on the following CDF from DCTCP/pFabric (Alizadeh et al., 2010/2013):
# ===
# CDF authors: Alizadeh et al.
# See also: https://github.com/datacenter/empirical-traffic-gen/blob/master/DCTCP_CDF
# Content:
# 0     0
# 10000 0.15
# 20000 0.2
# 30000 0.3
# 50000 0.4
# 80000 0.53
# 200000 0.6
# 1e+06 0.7
# 2e+06 0.8
# 5e+06 0.9
# 1e+07 0.97
# 3e+07 1
# ===
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

# Based on the following CDF from VL2/pFabric (Alizadeh et al., 2009/2013):
# ===
# CDF authors: Alizadeh et al.
# See also: https://github.com/datacenter/empirical-traffic-gen/blob/master/VL2_CDF
# Content:
# 0   0
# 180 0.1
# 216 0.2
# 560 0.3
# 900 0.4
# 1100 0.5
# 1870 0.6
# 3160 0.7
# 10000 0.8
# 400000 0.9
# 3.16e+06 0.95
# 1e+08 0.98
# 1e+09 1
# ===
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
