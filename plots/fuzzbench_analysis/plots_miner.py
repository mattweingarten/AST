import os

import pandas as pd

from fuzzbench_data import load_benchmarks, read_benchmarks_csv_list
from fuzzbench_plots import plot_all

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

D = SCRIPT_DIR + "/../../var/data/sancov/miner/miner"
data = [
    D + "/exp-2022-05-31-04-40-18-miner-lcms-2017/sancov_out.csv",
    D + "/exp-2022-05-27-17-46-55-libhtp_fuzz_htp/sancov_out.csv",
    D + "/exp-2022-05-30-23-14-50-curl_curl_fuzzer/sancov_out.csv",
    D + "/exp-2022-05-31-14-11-25-miner-libpng/sancov_out.csv",
    D + "/exp-2022-05-30-17-53-14-bloaty_fuzz_target/sancov_out.csv",
    D + "/exp-2022-06-02-09-48-52-miner-jsoncpp/sancov_out.csv",
    D + "/exp-2022-06-01-14-59-48-miner-libjpeg-turbo/sancov_out.csv",
    D + "/exp-2022-05-31-09-24-16-miner-libpcap_fuzz/sancov_out.csv",
    D + "/exp-2022-05-28-20-31-38-libhtp_fuzz_htp/sancov_out.csv",
    D + "/exp-2022-05-28-16-05-47-libhtp_fuzz_htp/sancov_out.csv",
    D + "/exp-2022-06-02-00-21-26-miner-freetype2-2017/sancov_out.csv",
    D + "/exp-2022-06-01-10-18-52-miner-vorbis-2017-12-11/sancov_out.csv",
    D + "/exp-2022-06-02-14-21-57-miner-lcms/sancov_out.csv",
    D + "/exp-2022-06-01-19-41-18-miner-harfbuzz/sancov_out.csv",
    D + "/exp-2022-05-30-13-01-21-freetype2-2017/sancov_out.csv",
    D + "/exp-2022-06-02-04-57-52-miner-bloaty/sancov_out.csv",
    D + "/exp-2022-06-02-18-53-53-miner-libpcap/sancov_out.csv",
    D + "/exp-2022-05-28-02-41-49-stb_stbi_read_fuzzer/sancov_out.csv",
    D + "/exp-2022-06-02-23-34-32-miner-libpng/sancov_out.csv",
]

if __name__ == '__main__':
    pd.set_option('display.max_rows', 100000)
    bms = read_benchmarks_csv_list(data)
    # bms = bms[(bms.fuzzer == "aflplusplus_ast_f0")]
    print(bms)

    plot_all(bms)
