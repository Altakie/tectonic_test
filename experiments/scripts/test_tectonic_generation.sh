#! /bin/bash
workloads=(
  "a"
  "b"
  "c"
  "d"
  "e"
  "f"
)

time="/usr/bin/time"
tectonic="$HOME/Tectonic/target/release/tectonic-cli"
db_path="/tmp/tectonic-rocksdb"
runs=5
# time=/usr/bin/time
# stats="$HOME/data/benchmarking/tectonic/rocksdb/1x/ycsb"
# spec_path="$HOME/workload_specs/tectonic/1x/"
scale=$1
# stats="$HOME/data/benchmarking/tectonic/rocksdb/${scale}x/ycsb"
stats="$HOME/data/generation/tectonic/${scale}x/ycsb/"
# spec_path="$HOME/workload_specs/tectonic/ycsb/${scale}x/"

cd $HOME/Tectonic
git switch no-marker-array
cargo build --release --features rocksdb

for wl in "${workloads[@]}"; do
  for run in $(seq 1 $runs); do
    prefix="${wl}/run${run}"
    log_path="$stats/$prefix.out"
    time_path="$stats/$prefix.time"
    cpu_log_path="$stats/$prefix.cpu"
    wl_out_path="$stats/$prefix.wl"

    sudo sysctl -w vm.drop_caches=3
    # rm -rf $db_path

    $time -v -o $time_path $tectonic generate \
      --ycsb $wl -s $scale -o $wl_out_path > >(tee $log_path) &
    pid="$!"

    sleep 0.1
    child_pid=$(pgrep -P $pid tectonic-cli)
    while ! ps -p $child_pid >/dev/null 2>&1; do sleep 0.01; done

    pidstat 1 -h -r -u -p $child_pid >"$cpu_log_path" &
    monitor_pid=$!

    wait $pid
    exit_code=$?
    kill $monitor_pid 2>/dev/null

    rm -f $wl_out_path

    if [[ $exit_code -ne 0 ]]; then
      echo "Something went wrong: workload $wl failed." | tee -a "$log_path"
    else
      echo ">>> Finished $wl Run $run"
    fi
    echo
  done
done

cd $HOME
