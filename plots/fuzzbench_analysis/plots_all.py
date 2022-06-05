import pandas as pd

from plots_bean import data as bean
from plots_miner import data as miner
from plots_matt import data as matt

from fuzzbench_data import load_benchmarks, read_benchmarks_csv_list
from fuzzbench_plots import plot_all

if __name__ == '__main__':
    data = bean + miner + matt
    pd.set_option('display.max_rows', 100000)
    bms = read_benchmarks_csv_list(data)

    bms = bms[(bms.benchmark != "libhtp_fuzz_htp")]
    bms = bms[(bms.benchmark != "stb_stbi_read_fuzzer")]
    print(bms)
    plot_all(bms)