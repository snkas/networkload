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

from .topology_type import Topology


def extend_tors_with_servers(topology, num_servers_per_tor):
    if num_servers_per_tor < 1:
        raise ValueError("Must extend with at least 1 server per ToR")
    if len(topology.servers) == 0 and len(topology.switches_which_are_tors) > 0:
        num_extra_nodes = len(topology.switches_which_are_tors) * num_servers_per_tor
        undirected_edges_list = list(topology.undirected_edges_list)
        node_id = topology.n
        for tor in topology.switches_which_are_tors:
            for i in range(num_servers_per_tor):
                undirected_edges_list.append((tor, node_id))
                node_id += 1
        return Topology(
            topology.n + num_extra_nodes,
            undirected_edges_list,
            topology.switches,
            topology.switches_which_are_tors,
            list(range(topology.n, topology.n + num_extra_nodes))
        )
    else:
        raise ValueError("There must be no servers and at least 1 ToR to be able to extend ToRs with servers.")
