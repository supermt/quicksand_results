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

    result_dir = "/home/supermt/ycsb_baseline_30X/"

    ycsb_workloads = ['a','b','c','d','e','f']
    for ycsb in ycsb_workloads:
        target_dir = result_dir + "/" + ycsb
        runner = DB_launcher(
            env, target_dir, db_bench=DEFAULT_DB_BENCH, extend_options={
                "key_size":24,
                "value_size":1000,
                "report_interval_seconds": 1,
                "mutable_compaction_thread_prior": "false",
                "benchmarks":"ycsb_load,ycsb_run,stats",
                "ycsb_workload":"ycsb_workload/workload"+ycsb,
                "histogram":True,
                # "statistics":True
    	        # "record_level_files": "true",
                # "change_points": "[{target_file_size_base,134217728,600},{write_buffer_size,134217728,600}]",
                #"DOTA_enabled":"true",
            })
        runner.run()
        reset_CPUs()
    clean_cgroup()
