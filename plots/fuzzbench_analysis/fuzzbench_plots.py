import os
from datetime import datetime

import pandas
import pandas as pd
import seaborn
from IPython.core.display import SVG
from matplotlib import pyplot, pyplot as plt

from analysis import data_utils, experiment_results, plotting
from analysis.data_utils import add_relative_columns, filter_benchmarks, filter_fuzzers
from fuzzbench_data import load_benchmarks


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
    # SVG(sqlite.coverage_growth_plot)
    # SVG(sqlite.mann_whitney_plot)
    # print(sqlite.mann_whitney_p_values)


def barplot(experiment_data):
    # print(experiment_data)
    fuzzer_names = experiment_data.fuzzer.unique()

    plotter = plotting.Plotter(fuzzer_names)
    results = experiment_results.ExperimentResults(experiment_data, None, '.', plotter)

    vals = {
        'benchmark': []
    }

    benchmarks = {b.name: b for b in results.benchmarks}
    for b in benchmarks:
        bench_data = filter_benchmarks(experiment_data, [b])

        fuzzers_in_bench_data = bench_data.fuzzer.unique()
        vals['benchmark'].append(b)

        for fuzz in fuzzers_in_bench_data:
            f = filter_fuzzers(bench_data, [fuzz])
            medians = f.groupby('fuzzer')['edges_covered'].median()

            key = medians.keys()[0]
            value = medians[0]
            if key not in vals:
                vals[key] = [value]
            else:
                vals[key].append(value)

    # df = pandas.DataFrame({
    #     'benchmark': ['A', 'B'],
    #     'fuzz0': [0.10, 0.20],
    #     'fuzz1': [0.15, 0.35],
    #     'fuzz2': [0.15, 0.35],
    # })
    df = pandas.DataFrame(vals)
    print(df)
    fig, ax1 = pyplot.subplots(figsize=(10, 15))
    tidy = df.melt(id_vars='benchmark').rename(columns=str.title)
    print(tidy)
    seaborn.barplot(x='Benchmark', y='Value', hue='Variable', data=tidy, ax=ax1)
    seaborn.despine(fig)
    plt.ylabel('Edge coverage')
    plt.xlabel('Benchmark')
    plt.xticks(rotation=45)
    plt.title('Edge Coverage (Median)')
    plt.legend(title='Fuzzer')

    # fig.show()
    fig.savefig('edge_cov.png')


def plot_all(experiment_data):
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    fuzzer_names = experiment_data.fuzzer.unique()
    plotter = plotting.Plotter(fuzzer_names)

    dir = SCRIPT_DIR + '/fuzzbench_plots/' + datetime.now().isoformat()
    os.makedirs(dir, exist_ok=True)

    results = experiment_results.ExperimentResults(experiment_data, None, dir, plotter)
    benchmarks = {b.name: b for b in results.benchmarks}
    print(benchmarks)


    cov = [b for b in results.benchmarks]
    for c in cov:
        print(c.type, c.name)

    results.critical_difference_plot


    for key in benchmarks.keys():
        benchmark = benchmarks[key]
        try:
            benchmark.fuzzers_with_not_enough_samples
        except:
            pass
        try:
            benchmark.summary_table
        except:
            pass
        try:
            benchmark.rank_by_mean
        except:
            pass
        try:
            benchmark.rank_by_median
        except:
            pass
        try:
            benchmark.rank_by_average_rank
        except:
            pass
        try:
            benchmark.rank_by_stat_test_wins
        except:
            pass
        try:
            benchmark.mann_whitney_p_values
        except:
            pass
        try:
            benchmark.bug_mann_whitney_p_values
        except:
            pass
        try:
            benchmark.vargha_delaney_a12_values
        except:
            pass
        try:
            benchmark.bug_vargha_delaney_a12_values
        except:
            pass
        try:
            benchmark.mann_whitney_plot
        except:
            pass
        try:
            benchmark.bug_mann_whitney_plot
        except:
            pass
        try:
            benchmark.vargha_delaney_plot
        except:
            pass
        try:
            benchmark.bug_vargha_delaney_plot
        except:
            pass
        try:
            benchmark.anova_p_value
        except:
            pass
        try:
            benchmark.anova_posthoc_p_values
        except:
            pass
        try:
            benchmark.anova_student_plot
        except:
            pass
        try:
            benchmark.anova_turkey_plot
        except:
            pass
        try:
            benchmark.kruskal_p_value
        except:
            pass
        try:
            benchmark.kruskal_posthoc_p_values
        except:
            pass
        try:
            benchmark.kruskal_conover_plot
        except:
            pass
        try:
            benchmark.kruskal_mann_whitney_plot
        except:
            pass
        try:
            benchmark.kruskal_wilcoxon_plot
        except:
            pass
        try:
            benchmark.kruskal_dunn_plot
        except:
            pass
        try:
            benchmark.kruskal_nemenyi_plot
        except:
            pass
        try:
            benchmark.coverage_growth_plot
        except:
            pass
        try:
            benchmark.coverage_growth_plot_logscale
        except:
            pass
        try:
            benchmark.violin_plot
        except:
            pass
        try:
            benchmark.bug_violin_plot
        except:
            pass
        try:
            benchmark.box_plot
        except:
            pass
        try:
            benchmark.bug_box_plot
        except:
            pass
        try:
            benchmark.distribution_plot
        except:
            pass
        try:
            benchmark.ranking_plot
        except:
            pass
        try:
            benchmark.better_than_plot
        except:
            pass
        try:
            benchmark.unique_coverage_ranking_plot
        except:
            pass
        try:
            benchmark.pairwise_unique_coverage_table
        except:
            pass
        try:
            benchmark.pairwise_unique_coverage_plot
        except:
            pass
        try:
            benchmark.bug_coverage_growth_plot_logscale
        except:
            pass
        try:
            benchmark.bug_coverage_growth_plot_logscale
        except:
            pass