import os

import pandas as pd

from fuzzbench_data import load_benchmarks, read_benchmarks_csv_list
from fuzzbench_plots import plot_all

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

D = SCRIPT_DIR + "/../../scripts/sancov_util_results"
data = [
# D + '/bloatyfuzztargetfoall1001/sancov_out.csv',
# D + '/bloatyfuzztargetopt1/sancov_out.csv',
# D + '/bloatyfuzztargetopto0o3/sancov_out.csv',
# D + '/lcms-2017-03-21foall1001/sancov_out.csv',
# D + '/lcms-2017-03-21opt1/sancov_out.csv',
# D + '/openthread-2019-12-23foall1001/sancov_out.csv',
# D + '/openthread-2019-12-23opt2/sancov_out.csv',
# D + '/openthread-2019-12-23opto0o3/sancov_out.csv',
# D + '/sqlite3ossfuzzfoall1001/sancov_out.csv',
# D + '/sqlite3ossfuzzopt2/sancov_out.csv',
# D + '/sqlite3ossfuzzopto0o3/sancov_out.csv',
D + '/woff2-2016-05-06foall1001/sancov_out.csv',
D + '/woff2-2016-05-06opt2/sancov_out.csv',
D + '/woff2-2016-05-06opto0o3/sancov_out.csv',

# D +  '/bloatyfuzztargetpreseeded1/sancov_out.csv',
# D +  '/lcms-2017-03-21preseeded1/sancov_out.csv',
# D +   '/sqlite3ossfuzzpreseeded1/sancov_out.csv',
D +   '/woff2-2016-05-06preseeded1/sancov_out.csv'
]

if __name__ == '__main__':
    pd.set_option('display.max_rows', 100000)
    bms = read_benchmarks_csv_list(data)
    # bms = bms[(bms.fuzzer == "aflplusplus_ast_f0")]
    print(bms)

    plot_all(bms)
