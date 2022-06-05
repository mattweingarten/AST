# XXX: must run in virutal env of fuzzbench

import os
import socket
import sys
import pandas as pd

from analysis.data_utils import filter_benchmarks, filter_fuzzers

pd.set_option('expand_frame_repr', False)

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
os.makedirs(PLOT_DIR, exist_ok=True)

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
    make_coverage_monotonic(experiment_data)
    return experiment_data


def make_coverage_monotonic(df):
    if df is None:
        return

    exp = None
    bench = None
    fuz = None
    trial = None
    first = True
    for index, row in df.iterrows():
        if first:
            first = False
        else:
            if exp == row['experiment']:
                if bench == row['benchmark']:
                    if fuz == row['fuzzer']:
                        if trial == row['trial_id']:
                            row['edges_covered'] = max(row['edges_covered'], df.iloc[index - 1].at['edges_covered'])
                            pass

        exp = row['experiment']
        bench = row['benchmark']
        fuz = row['fuzzer']
        trial = row['trial_id']


def read_benchmarks_csv_list(csv_paths):
    experiment_data = None
    for path in csv_paths:
        try:
            data = pd.read_csv(path)
        except Exception as e:
            print(path, ' not found')
            continue

        if experiment_data is None:
            experiment_data = data
        else:
            experiment_data = pd.concat([experiment_data, data], axis=0)
    print(experiment_data)
    make_coverage_monotonic(experiment_data)
    return experiment_data

def load_benchmarks():
    """
    Load fuzzbench data.csv files
    """

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
        'exp-2022-04-26-15-20-12-vorbis-2017-12-11_1h'
    ]

    experiment_data_1 = read_benchmarks(home_bean, benchmarks_bean)
    experiment_data = pd.concat([experiment_data_0, experiment_data_1], axis=0)
    return experiment_data

def clean_up_data(experiment_data):
    """
    Clean up data into unified csv file
    """
    fuzzer_names = experiment_data.fuzzer.unique()

    plotter = plotting.Plotter(fuzzer_names)
    results = experiment_results.ExperimentResults(experiment_data, None, '.', plotter)
    benchmarks = {b.name: b for b in results.benchmarks}

    rows = []
    for b in benchmarks:
        bench_data = filter_benchmarks(experiment_data, [b])
        fuzzers_in_bench_data = bench_data.fuzzer.unique()

        def get_key_val(res):
            return res.keys()[0], res[0]

        for fuzz in fuzzers_in_bench_data:
            f = filter_fuzzers(bench_data, [fuzz])

            medians = f.groupby('fuzzer')['edges_covered'].median()
            means = f.groupby('fuzzer')['edges_covered'].mean()
            maxs = f.groupby('fuzzer')['edges_covered'].max()
            mins = f.groupby('fuzzer')['edges_covered'].min()

            times = f.groupby('fuzzer')['time'].max()

            fuzzer_name, median = get_key_val(medians)
            _, mean = get_key_val(means)
            _, max = get_key_val(maxs)
            _, min = get_key_val(mins)
            _, time = get_key_val(times)

            exp = bench_data.experiment[0]

            # id, benchmark-name, fuzzer name,
            rows.append([exp, b, fuzz, mean, median, max, min, time])

    df = pd.DataFrame(rows,
                      columns=['Experiment', 'benchmark', 'fuzzer', 'edgecov-mean', 'edgecov-median', 'edgecov-max',
                               'edgecov-min', 'time'])

    df.to_csv('./experiment_result_cleaned.csv')


if __name__ == '__main__':
    experiment_data = load_benchmarks()
    clean_up_data(experiment_data)
