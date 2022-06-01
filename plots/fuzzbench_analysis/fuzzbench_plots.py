import os
from datetime import datetime

import pandas
import pandas as pd
import seaborn
from IPython.core.display import SVG
from matplotlib import pyplot, pyplot as plt

from analysis import data_utils, experiment_results, plotting
from analysis.data_utils import add_relative_columns, filter_benchmarks, filter_fuzzers
from fuzzbench_data import load_benchmark_post_processing, load_benchmarks


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
    plt.legend(title = 'Fuzzer')

    # fig.show()
    fig.savefig('edge_cov.png')


def plot_all(experiment_data):
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    fuzzer_names = experiment_data.fuzzer.unique()
    plotter = plotting.Plotter(fuzzer_names)

    dir = SCRIPT_DIR + '/fuzzbench_plots/' + datetime.now().isoformat()
    os.makedirs(dir, exist_ok= True)

    results = experiment_results.ExperimentResults(experiment_data, None, dir, plotter)
    benchmarks = {b.name: b for b in results.benchmarks}

    results.critical_difference_plot
    pass

    for key in benchmarks.keys():
        benchmark = benchmarks[key]
        benchmark.fuzzers_with_not_enough_samples
        benchmark.summary_table
        benchmark.rank_by_mean
        benchmark.rank_by_median
        benchmark.rank_by_average_rank
        benchmark.rank_by_stat_test_wins
        benchmark.mann_whitney_p_values
        # benchmark.bug_mann_whitney_p_values
        benchmark.vargha_delaney_a12_values
        # benchmark.bug_vargha_delaney_a12_values
        benchmark.mann_whitney_plot
        # benchmark.bug_mann_whitney_plot
        benchmark.vargha_delaney_plot
        # benchmark.bug_vargha_delaney_plot
        benchmark.anova_p_value
        benchmark.anova_posthoc_p_values
        benchmark.anova_student_plot
        benchmark.anova_turkey_plot
        benchmark.kruskal_p_value

        benchmark.kruskal_posthoc_p_values
        benchmark.kruskal_conover_plot
        benchmark.kruskal_mann_whitney_plot
        benchmark.kruskal_wilcoxon_plot
        benchmark.kruskal_dunn_plot
        benchmark.kruskal_nemenyi_plot

        benchmark.coverage_growth_plot
        benchmark.coverage_growth_plot_logscale
        benchmark.violin_plot
        # benchmark.bug_violin_plot
        benchmark.box_plot
        # benchmark.bug_box_plot
        benchmark.distribution_plot
        benchmark.ranking_plot
        benchmark.better_than_plot

        # benchmark.unique_coverage_ranking_plot
        # benchmark.pairwise_unique_coverage_table
        # benchmark.pairwise_unique_coverage_plot
        # benchmark.bug_coverage_growth_plot_logscale
        # benchmark.bug_coverage_growth_plot_logscale



if __name__ == '__main__':
    # data = load_benchmarks()
    data = load_benchmark_post_processing()
    # fuzzbench_analysis(data)
    # barplot(data)
    plot_all(data)

    pass
