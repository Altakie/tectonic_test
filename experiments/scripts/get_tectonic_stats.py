import os
import sys


scale = int(sys.argv[1])

HOME = os.getenv("HOME")
STATS = f"{HOME}/data/benchmarking/tectonic/rocksdb/{scale}x/ycsb"
OP_COUNT = 2000000 * scale
RUNS = 5


# stats = sys.argv[1]

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


def get_stats(workload_path: str, workload_name: str):
    total_time = 0
    total_peak_memory = 0
    for file in os.listdir(workload_path):
        file_split = file.split(".")
        if len(file_split) < 2:
            continue
        file_extension = file_split[1]
        real_file = os.path.join(workload_path, file)
        with open(real_file, "r") as f:
            lines = f.readlines()
            if file_extension == "time":
                # Get wall time
                for line in lines:
                    if "Elapsed (wall clock) time" in line:
                        time = line.split("): ")[1]
                        times = time.split(":")
                        mins = int(times[0])
                        seconds = float(times[1])
                        seconds += float(mins) * 60.0
                        total_time += seconds
            elif file_extension == "cpu":
                # Get RSS memory
                peak = 0
                lines = lines[1:]
                for line in lines:
                    if "RSS" in line:
                        continue
                    if line.strip() == "":
                        continue
                    line_split = line.split()
                    rss_mem = int(line_split[12])
                    if rss_mem > peak:
                        peak = rss_mem
                total_peak_memory += peak
            else:
                continue
    averaged_stats[workload_name] = {
        "Average End-To-End Latency": total_time / RUNS,
        "Average_Peak_RSS": total_peak_memory / RUNS,
        "Average Throughput": OP_COUNT * RUNS / total_time,
    }


for path, workloads, _ in os.walk(STATS):
    for workload in workloads:
        get_stats(os.path.join(path, workload), workload)

print(averaged_stats)
