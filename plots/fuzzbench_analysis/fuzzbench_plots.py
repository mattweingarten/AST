# XXX: must run in virutal env of fuzzbench

import os
import socket
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.display import SVG

if socket.gethostname() == 'localhost.localdomain':
    # Andrin's device
    FUZZBENCH_HOME = '/home/b/bdata/beandata/eth/projects_eth/eth-sm04-ast/repo/matt-fuzzbench'
else:
    FUZZBENCH_HOME = 'TODO'

sys.path.append(FUZZBENCH_HOME)

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_HOME = SCRIPT_DIR + '/../../'
PLOT_DIR = SCRIPT_DIR + '/plot_out/./'
try:
    os.makedirs(PLOT_DIR, exist_ok=True)
except:
    pass

pd.set_option('expand_frame_repr', False)

from analysis import data_utils, experiment_results, plotting

def read_benchmarks(home_path, benchmark_dir_names):
    experiment_data = None
    for b in benchmark_dir_names:
        path = home_path + '/' + b + '/data.csv.gz'
        try:
            data = pd.read_csv(path)
        except Exception as e:
            print(path, ' not found')
            data = pd.read_csv(home_path + '/' + b + '/data.csv')

        if experiment_data is None:
            experiment_data = data
        else:
            experiment_data = pd.concat([experiment_data, data], axis=0)
    return experiment_data


def load_benchmarks():
    home_mat = REPO_HOME + 'wmatt/report-data'
    benchmarks_matt = [
        'bloatyfuzztarget-all4hours1'
        , 'lcms-2017-03-21-all4hours1'
        , 'libxml2-v292-all4hours1'
        , 'openthread-2019-12-23-all'
        , 'sqlite3ossfuzz-all4hours1'
        , 'woff2-2016-05-06-all']

    experiment_data_0 = read_benchmarks(home_mat, benchmarks_matt)

    home_bean = REPO_HOME + 'bean/benchmarks/report-data'
    benchmarks_bean = [
        'exp-2022-04-22-00-58-08-libpng-1.2.56-4h-p52-thinkpad',
        'exp-2022-04-21-23-01-44-freetype2-1h-p52-thinkpad',
        # 'exp-2022-04-21-21-12-44-aspell-1h-p52-thinkpad'
    ]

    experiment_data_1 = read_benchmarks(home_bean, benchmarks_bean)
    experiment_data = pd.concat([experiment_data_0, experiment_data_1], axis=0)
    return experiment_data


def fuzzbench_analysis(experiment_data):
    # Load the data and initialize ExperimentResults.
    fuzzer_names = experiment_data.fuzzer.unique()

    plotter = plotting.Plotter(fuzzer_names)
    results = experiment_results.ExperimentResults(experiment_data, None, '.', plotter)

    ## Top level results
    print(results.summary_table)
    print('print(results.rank_by_median_and_average_rank.to_frame())')
    print(results.rank_by_median_and_average_rank.to_frame())
    print('results.rank_by_stat_test_wins_and_average_rank.to_frame()')
    print(results.rank_by_stat_test_wins_and_average_rank.to_frame())
    print('results.rank_by_median_and_average_normalized_score.to_frame()')
    print(results.rank_by_median_and_average_normalized_score.to_frame())
    print('results.rank_by_average_rank_and_average_rank.to_frame()')
    print(results.rank_by_average_rank_and_average_rank.to_frame())
    print('print(results.rank_by_mean_and_average_rank.to_frame())')
    print(results.rank_by_mean_and_average_rank.to_frame())
    print('print(results.rank_by_median_and_number_of_firsts.to_frame())')
    print(results.rank_by_median_and_number_of_firsts.to_frame())
    print('\nbenchmarks:')
    benchmarks = {b.name: b for b in results.benchmarks}
    for benchmark_name in benchmarks.keys(): print(benchmark_name)

    # %%
    # sqlite = benchmarks['sqlite3_ossfuzz']
    # SVG(sqlite.violin_plot)
    # SVG(sqlite.coverage_growth_plot)
    # SVG(sqlite.mann_whitney_plot)
    # print(sqlite.mann_whitney_p_values)


if __name__ == '__main__':
    experiment_data = load_benchmarks()


