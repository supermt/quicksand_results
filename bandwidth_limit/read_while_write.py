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

    device_list = parameter_dict["storage_paths"]

    io_bandwidth_list=[400,800]

    result_dir = "pm_results_bandwidth/read_while_write/"

    os.system("cgcreate -g blkio:/test_group1")
    for io_bandwidth in io_bandwidth_list:
        for device_info in device_list:

            os.system('cgset -r blkio.throttle.write_bps_device="'+device_info["device_id"]+' '+str(io_bandwidth*1024*1024)+'" test_group1')
        # test for the limiting
        os.system('cat /sys/fs/cgroup/blkio/test_group1/blkio.throttle.write_bps_device')


        benchmark_opt =  {
                "num":120*1000*1000,
                "report_interval_seconds": 1,
                "value_size":1000,
                "key_size":16,
                "subcompactions":20,
                "benchmarks":"readwhilewriting,stats",
                "report_bg_io_stats":"true",
            }
        temp_result_dir = result_dir+str(io_bandwidth) +"/"
        runner = DB_launcher(
            env, temp_result_dir, db_bench=DEFAULT_DB_BENCH, extend_options=benchmark_opt)
        runner.run()
        reset_CPUs()

    os.system("cgdelete blkio:/test_group1")
    clean_cgroup()
