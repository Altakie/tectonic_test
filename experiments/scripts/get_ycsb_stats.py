import os


HOME = os.getenv("HOME")
STATS = f"{HOME}/data/benchmarking/ycsb/rocksdb/1x/"
OP_COUNT = 2000000
RUNS = 5

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
        file_extension = file[1]
        with open(file, "r") as f:
            lines = f.readlines()
            if file_extension == "time":
                # Get wall time
                for line in lines:
                    if "Elapsed (wall clock time)" in line:
                        time = line.split("): ")[1]
                        times = time.split(":")
                        mins = int(times[0])
                        seconds = float(times[1])
                        seconds += float(mins) * 60.0
                        total_time += seconds
            elif file_extension == "cpu":
                # Get RSS memory
                peak = 0
                for line in lines:
                    if "RSS" in line:
                        continue
                    rss_mem = int(line[12])
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
