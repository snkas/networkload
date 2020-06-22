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


def write_topology(filename, topology):
    with open(filename, "w+") as f_out:
        f_out.write("num_nodes=" + str(topology.n) + "\n")
        f_out.write("num_undirected_edges=" + str(len(topology.undirected_edges_list)) + "\n")
        f_out.write("switches=set(" + ','.join(str(x) for x in topology.switches) + ")\n")
        f_out.write("switches_which_are_tors=set(" + ','.join(str(x) for x in topology.switches_which_are_tors) + ")\n")
        f_out.write("servers=set(" + ','.join(str(x) for x in topology.servers) + ")\n")
        f_out.write("undirected_edges=set("
                    + ','.join(str(x[0]) + "-" + str(x[1]) for x in topology.undirected_edges_list)
                    + ")\n")
