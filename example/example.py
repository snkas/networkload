from networkload import *

#########################################################

# Topology
# Options: fat_tree_symmetric, fat_tree_asymmetric, leaf_spine, plus_grid
topology = extend_tors_with_servers(leaf_spine(4, 4), 2)

# Write topology
write_topology(
    "topology.properties",
    topology
)

#########################################################

# Core values
duration_ns = 10 * 1000 * 1000 * 1000  # 10 seconds
expected_flows_per_s = 100
random.seed(123456789)
seed_start_times = random.randint(0, 100000000)
seed_from_to = random.randint(0, 100000000)
seed_flow_size = random.randint(0, 100000000)

# Start times (ns)
list_start_time_ns = draw_poisson_inter_arrival_gap_start_times_ns(duration_ns, expected_flows_per_s, seed_start_times)
num_starts = len(list_start_time_ns)

# (From, to) tuples
list_from_to = draw_n_times_from_to_all_to_all(num_starts, topology.servers, seed_from_to)

# Flow sizes in byte
list_flow_size_byte = list(
    round(x) for x in draw_n_times_from_cdf(num_starts, CDF_PFABRIC_WEB_SEARCH_BYTE, True, seed_flow_size)
)

# Write schedule
write_schedule(
    "schedule.csv",
    num_starts,
    list_from_to,
    list_flow_size_byte,
    list_start_time_ns
)
