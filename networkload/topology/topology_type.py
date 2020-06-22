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


class Topology:

    def __init__(self, n, undirected_edges_list, switches, switches_which_are_tors, servers):

        # Adjacency list
        self.adjacency_list = {}
        for i in range(n):
            self.adjacency_list[i] = set()
        new_undirected_edges_list = []
        new_undirected_edges_set = set()
        for edge in undirected_edges_list:

            # Valid endpoints
            if edge[0] < 0 or edge[0] >= n or edge[1] < 0 or edge[1] >= n or edge[0] == edge[1]:
                raise ValueError("Invalid edge endpoints: " + str(edge))

            # We want them (a, b) with a < b
            ordered_edge = (
                edge[0] if edge[0] < edge[1] else edge[1],
                edge[1] if edge[1] > edge[0] else edge[0]
            )

            # Edge cannot already exist
            if ordered_edge in new_undirected_edges_set:
                raise ValueError("Cannot have two the same edges: " + str(edge))

            # Add them
            new_undirected_edges_list.append(ordered_edge)
            new_undirected_edges_set.add(ordered_edge)
            self.adjacency_list[ordered_edge[0]].add(ordered_edge[1])
            self.adjacency_list[ordered_edge[1]].add(ordered_edge[0])

        new_undirected_edges_list = sorted(new_undirected_edges_list)

        # Duplicate entries
        if len(set(switches)) != len(switches):
            raise ValueError("Duplicate switches present in list")
        switches = set(switches)
        if len(set(switches_which_are_tors)) != len(switches_which_are_tors):
            raise ValueError("Duplicate switches_which_are_tors present in list")
        switches_which_are_tors = set(switches_which_are_tors)
        if len(set(servers)) != len(servers):
            raise ValueError("Duplicate servers present in list")
        servers = set(servers)

        # Not valid identifiers
        all_node_ids = set(range(n))
        if all_node_ids.intersection(switches) != switches:
            raise ValueError("Invalid id in switches")
        if all_node_ids.intersection(switches_which_are_tors) != switches_which_are_tors:
            raise ValueError("Invalid id in switches_which_are_tors")
        if all_node_ids.intersection(servers) != servers:
            raise ValueError("Invalid id in servers")

        # Servers and switches must be distinct
        if not len(servers.intersection(switches)) == 0:
            raise ValueError("Server and switch identifiers are not distinct: " + str(servers.intersection(switches)))

        # A node is either a switch or a server
        if servers.union(switches) != all_node_ids:
            raise ValueError("Server and switch identifiers are not distinct")

        # Only switches can be ToRs
        if switches.intersection(switches_which_are_tors) != switches_which_are_tors:
            raise ValueError("Server and switch identifiers are not distinct")

        # Servers can only be connected to a ToR
        degree_counter = [0]*n
        for edge in new_undirected_edges_list:
            degree_counter[edge[0]] += 1
            degree_counter[edge[1]] += 1
            if edge[0] in servers:
                if edge[1] not in switches_which_are_tors:
                    raise ValueError(
                        "Server node " + str(edge[0]) + " has an edge to a node " + str(edge[1]) + " which is not a ToR"
                    )
            if edge[1] in servers:
                if edge[0] not in switches_which_are_tors:
                    raise ValueError(
                        "Server node " + str(edge[1]) + " has an edge to a node " + str(edge[0]) + " which is not a ToR"
                    )

        # Servers can only be connected to one ToR
        for s in servers:
            if degree_counter[s] != 1:
                raise ValueError("Server must exactly have one edge to a ToR. Server " + str(s) + " does not.")

        # No duplicates, so we can at least set the properties
        self.n = n
        self.undirected_edges_list = list(new_undirected_edges_list)
        self.undirected_edges_set = new_undirected_edges_set
        self.switches = switches
        self.switches_which_are_tors = switches_which_are_tors
        self.servers = servers

    def __str__(self):
        return "Topology(#nodes=%d (%d switches (of which %d are ToRs), %d servers), #edges=%d)" % (
            self.n,
            len(self.switches),
            len(self.switches_which_are_tors),
            len(self.servers),
            len(self.undirected_edges_set)
        )
