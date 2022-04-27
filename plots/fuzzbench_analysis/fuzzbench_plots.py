from analysis import experiment_results, plotting
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
    # SVG(sqlite.violin_plot)
    # SVG(sqlite.coverage_growth_plot)
    # SVG(sqlite.mann_whitney_plot)
    # print(sqlite.mann_whitney_p_values)


if __name__ == '__main__':
    data = load_benchmarks()
    fuzzbench_analysis(data)
    pass
