import os

import pandas as pd

from fuzzbench_data import load_benchmarks, read_benchmarks_csv_list
from fuzzbench_plots import plot_all

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

D = SCRIPT_DIR + "/../../var/data/sancov/bean/"

data = [
D + 'exp-2022-05-27-19-08-48-vorbis/sancov_out.csv',
D + 'exp-2022-05-28-00-17-12-libjpeg/sancov_out.csv',
D + 'exp-2022-05-28-23-07-05-harfbuzz-1.3.2/sancov_out.csv',
D + 'exp-2022-05-29-18-46-52-bean-g1-freetype2-2017/sancov_out.csv',
D + 'exp-2022-05-29-23-21-18-bean-g1-bloaty_fuzz/sancov_out.csv',
D + 'exp-2022-05-30-04-33-01-bean-g1-curl_curl-12-snapshots/sancov_out.csv',
D + 'exp-2022-06-01-11-56-41-bean-all-vorbis-2017-12-11/sancov_out.csv',
D + 'exp-2022-06-01-16-25-12-bean-all-freetype2-2017/sancov_out.csv',
D + 'exp-2022-06-01-22-52-21-bean-all-vorbis-2017-12-11/sancov_out.csv',
D + 'exp-2022-06-02-18-31-30-bean-all-vorbis-2017-12-11/sancov_out.csv',
D + 'exp-2022-06-03-16-18-20-bean-all-freetype2-2017/sancov_out.csv',
D + 'exp-2022-06-03-21-57-58-bean-all-libjpeg-turbo-07-2017/sancov_out.csv',

# Too much, create dedicated plots for this
# D + '../bean-from_input_seed/sancov_util_results/exp-2022-06-06-00-44-39-freetype2/sancov_out.csv',
# D + '../bean-from_input_seed/sancov_util_results/exp-2022-06-06-00-44-39-libjpeg/sancov_out.csv',
# D + '../exp-2022-06-06-00-44-39-vorbis/sancov_out.csv'



]




if __name__ == '__main__':
    pd.set_option('display.max_rows', 100000)
    bms = read_benchmarks_csv_list(data)
    # bms = bms[(bms.fuzzer == "aflplusplus_ast_f0")]
    print(bms)

    plot_all(bms)
