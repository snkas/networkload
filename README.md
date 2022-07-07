# Networkload

[![Build Status](https://travis-ci.com/snkas/networkload.svg?branch=master)](https://travis-ci.com/snkas/networkload) [![codecov](https://codecov.io/gh/snkas/networkload/branch/master/graph/badge.svg)](https://codecov.io/gh/snkas/networkload)

This Python module encompasses functions used to generate workloads for networks. There is a distinction between topology and schedule generation.

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. (see also the MIT License in ./LICENSE).**

**Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. (see also the Apache License v2.0 in ./LICENSE).**

## Installation

**Requirements**
* Python 3.6+
* `pip install numpy`

**Option 1**

```bash
$ pip install git+https://github.com/snkas/networkload.git
```

You can now include it using: `import networkload`

**Option 2**

Clone/download this Git repository. Then, execute the following to install the package locally:

```bash
$ bash install_local.sh
```

You can now include it using: `import networkload`


## Getting started

1. Go to example directory: `cd example`
2. Run example: `python example.py`
3. This will generate two files: `topology.properties` and `schedule.csv`


## Current state

**Topologies**
* Fat-tree (symmetric or asymmetric aggregation-core links)
* Leaf-spine
* Plus-grid

**Schedule**
* From-to all-to-all
* From-to random-pairing
* Poisson arrival
* Constant arrival
* Constant flow size
* Flow size from CDF. The CDF database includes an interpretation of pFabric web search and pFabric data mining CDFs. These CDFs are licensed under Apache License v2.0 by pFabric/DCTCP/VL2's authors, see also:
  - https://github.com/datacenter/empirical-traffic-gen
  - https://github.com/snkas/networkload/blob/master/networkload/schedule/flowsize/flow_size_cdf_database.py


## Formats

**Topology format (.properties)**
```
num_nodes=<n, e.g. 5>
num_undirected_edges=<m, e.g., 4>
switches=set(<comma-separated list of node identifiers [0, n), e.g. 1,2,3>)
switches_which_are_tors=set(<comma-separated list of node identifiers [0, n), e.g. 1,3>)
servers=set(<comma-separated list of node identifiers [0, n), e.g. 0,4>)
undirected_edges=set(<comma-separated list of edges as a-b, e.g. 0-1,1-2,2-3,3-4>)
```

... with the following rules:
* A node must be either a switch or a server
* A switch can be a ToR
* A server must have exactly one connection to a ToR
* If there are no servers, only ToRs are valid endpoints for flows, else only servers are

**Schedule format (.csv)**
```
flow_id,from_node_id,to_node_id,size_byte,start_time_ns,additional_parameters,metadata
```


## Testing

Run all tests (local version):
```bash
$ python -m pytest
```

Run all tests (global pip-installed version):
```bash
$ pytest
```

Calculate coverage locally (output in `htmlcov/`):
```bash
$ bash calculate_coverage.sh
```
