import os
import sys

work_path = os.getcwd()
os.chdir("../")
print(os.getcwd())
sys.path.insert(0, '.')

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_option import load_config_file
from db_bench_option import set_parameters_to_env
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial
from db_bench_runner import clean_cgroup

os.chdir(work_path)
if __name__ == '__main__':
    env = HardwareEnvironment()
    parameter_dict = load_config_file('config.json')
    set_parameters_to_env(parameter_dict, env)

    result_dir = "pm_results_ycsb_zipfian"

    runner = DB_launcher(
        env, result_dir, db_bench=DEFAULT_DB_BENCH, extend_options={
            "key_size":16,
            "value_size":1000,
            "report_interval_seconds": 1,
            "load_num":10*1000*1000,
            "running_num":10*1000*1000,
            "benchmarks":"ycsb_load,ycsb_run,stats",
            "ycsb_workload":"ycsb_workload/workloada_zipfian",
            "histogram":True,
            "statistics":True
        })
    runner.run()
    reset_CPUs()
    clean_cgroup()
