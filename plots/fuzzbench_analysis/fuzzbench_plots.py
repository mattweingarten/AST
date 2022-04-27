import pandas
import seaborn
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
    plt.title('Edges Covered median')

    fig.show()


if __name__ == '__main__':
    data = load_benchmarks()
    # fuzzbench_analysis(data)
    barplot(data)
    pass
