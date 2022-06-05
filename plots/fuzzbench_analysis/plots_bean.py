import pandas as pd

from fuzzbench_data import load_benchmarks, read_benchmarks_csv_list
from fuzzbench_plots import plot_all

data = [
]




if __name__ == '__main__':
    pd.set_option('display.max_rows', 100000)
    bms = read_benchmarks_csv_list(data)
    # bms = bms[(bms.fuzzer == "aflplusplus_ast_f0")]
    print(bms)

    plot_all(bms)
