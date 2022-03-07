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

    result_dir = "pm_results_1000_bytes/write_read_write/"

    benchmark_opt =  {
            "num":20*1000*1000,
            "report_interval_seconds": 1,
            "value_size":1000,
            "key_size":16,
            "subcompactions":20,
            "reads":10000,
            "mutable_compaction_thread_prior": "false",
            "benchmarks":"fillrandom,readrandom,stats",
            "report_bg_io_stats":"true",
            #"DOTA_enabled":"true",
        }
    temp_result_dir = result_dir +"/"
    runner = DB_launcher(
        env, temp_result_dir, db_bench=DEFAULT_DB_BENCH, extend_options=benchmark_opt)
    runner.run()
    reset_CPUs()
    clean_cgroup()
