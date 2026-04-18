import os

STATS = "$HOME/data/benchmarking/tectonic/rocksdb/1x/ycsb"
OP_COUNT = 2000000

"""
For each workload, go through each run
From the time file, get the wall time in seconds
From the cpu file, get the peak RSS memory
    To get the peak RSS memory, go through all the RSS memories and take the max
Save the average for each workload in a hashmap
Calculate the throughput for each workload
Print all values in the hashmap
"""

averaged_stats = {}

# def get_stats(workload_path):
#     for path, _, files in os.walk(workload_path):
#
#         file_split = file.


for path, _, file in os.walk(STATS):
    print(file)
