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


def write_schedule(filename, num_starts, list_from_to, list_flow_size_byte, list_start_time_ns,
                   list_extra_parameters=None, list_metadata=None):
    """
    Write schedule to file.

    :param filename:
    :param num_starts:                  Expected number of values in all lists
    :param list_from_to:                List of (from, to)-tuples
    :param list_flow_size_byte:         List of integer flow size (byte)
    :param list_start_time_ns:          List of integer start times (ns)
    :param list_extra_parameters:       List of strings (can be anything, just not containing a comma)
    :param list_metadata:               List of strings (can be anything, just not containing a comma)
    """

    if num_starts < 1:
        raise ValueError("Cannot have an empty schedule")
    if len(list_from_to) != num_starts:
        raise ValueError("length(list_from_to) = " + str(len(list_from_to)) + " != " + str(num_starts))
    if len(list_flow_size_byte) != num_starts:
        raise ValueError("length(list_flow_size) = " + str(len(list_flow_size_byte)) + " != " + str(num_starts))
    if len(list_start_time_ns) != num_starts:
        raise ValueError("length(list_start_time) = " + str(len(list_start_time_ns)) + " != " + str(num_starts))
    if list_extra_parameters is not None and len(list_extra_parameters) != num_starts:
        raise ValueError(
            "length(list_extra_parameters) = " + str(len(list_extra_parameters)) + " != " + str(num_starts)
        )
    if list_metadata is not None and len(list_metadata) != num_starts:
        raise ValueError("length(list_metadata) = " + str(len(list_metadata)) + " != " + str(num_starts))

    with open(filename, "w+") as f_out:
        for i in range(num_starts):
            f_out.write("%d,%d,%d,%d,%d,%s,%s\n" % (
                i,
                list_from_to[i][0],
                list_from_to[i][1],
                list_flow_size_byte[i],
                list_start_time_ns[i],
                list_extra_parameters[i] if list_extra_parameters is not None else "",
                list_metadata[i] if list_metadata is not None else ""
            ))
