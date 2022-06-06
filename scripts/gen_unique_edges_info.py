from argparse import ArgumentParser
from util import * 
import os
import csv
import pandas as pd
import subprocess
import io

# def handle_exp(exp):
#     runs = [f.path for f in os.scandir(exp) if f.is_dir()]
#     for run in runs:
#         try:
#             handle_data(os.path.join(run,"data"))
#         except: 
#             try: 
#                 handle_data(os.path.join(run,"coverage","data"))
#             except Exception as e:
#                 print(e)
#                 print("Couldnt parse data.." + run)
COVERED_EDGES = {

}

def read_sancov(f):
    print(f)

    if FOREIGN:
        if "miner" in f :
            f = f.replace("/home/b/bdata-unsync/ast-fuzz/miner/miner-experiment-data/sancov_util_results/", "/mnt/c/Users/Matt/Desktop/ASTtop/AST/var/data/sancov/miner/miner/")
        else:
            f = f.replace("/home/b/bdata-unsync/ast-fuzz/experiment-data/o0_coverage/sancov_util_results/","/mnt/c/Users/Matt/Desktop/ASTtop/AST/var/data/sancov/bean/" )

    # print(f)
    # exit(1)
    edges = set()

    proc = subprocess.Popen(['sancov', '--print',f],stdout=subprocess.PIPE)
    # proc.wait()

    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):  # or another encoding
        # print(line.rstrip())
        edges.add(int(line, 16))
    return edges

def handle_exp(path):
    try:
        df = pd.read_csv(path + "/sancov_out.csv")
        handle_trial(df)
        # print(df)
    except Exception as e: 
        print("Couldn't read " + path +  " E:" + str(e))

def handle_results(path):
        bs = [f.path for f in os.scandir(path) if f.is_dir()]
        for b in bs: 
            handle_exp(b) 


def handle_trial(df):
    # print(df.columns.values)
    # df = df[['corpusNr', 'fuzzer' ,'benchmark','sancov_file']]
    # print(df)
    # print(df['corpusNr'])
    # print(df.query('corpusNr == 17'))
    df = df.query('corpusNr == 17')
    # print(COVERED_EDGES)

    df = df.reset_index()  # make sure indexes pair with number of rows
    for index, row in df.iterrows():

        # print(row['fuzzer'], row['benchmark'], row['sancov_file'])
        set = read_sancov(row['sancov_file'])

        key = (row['fuzzer'], row['benchmark'])

        if(key in COVERED_EDGES.keys()):
            COVERED_EDGES[key] = COVERED_EDGES[key].union(set)
        else:
            COVERED_EDGES[key] = set
    # print(COVERED_EDGES.keys())
    # exit(0)

    # df2 = df.groupby()

    # bench_flag_pairs = [f.path for f in os.scandir(trial) if f.is_dir()]
    # bf_pairs = [(get_benchmark(b_f_pair,BENCHMARKS),get_flag(b_f_pair,FLAGS)) for b_f_pair in bench_flag_pairs]
    # covered_regions_dict = {}
    # for b_f_pair in bench_flag_pairs:
    #     bench,flag = bench,flag = get_benchmark(b_f_pair,BENCHMARKS),get_flag(b_f_pair,FLAGS)
    #     cov = get_exp_json(b_f_pair + "/covered_regions.json")
    #     cov_set = set()
    #     for region in cov:
    #         cov_set.add(tuple(region))
    #     covered_regions_dict[concat(bench,flag)] = cov_set


    # for (l_b,l_f) in bf_pairs:
    #     for (r_b,r_f) in bf_pairs:
            # diff = get_num_regions_without((l_b,l_f),(r_b,r_f),covered_regions_dict)
    #         CSV_WRITER.writerow([l_b,l_f,r_b,r_f, diff])

    
# def get_num_regions_without(bf1,bf2,covered_regions_dict):
#     return len(covered_regions_dict[bf1] - covered_regions_dict[bf2])

#Main
parser = ArgumentParser()
# parser.add_argument('--exp_folders',nargs='+', default=["wmatt/experiment-data", "bean/benchmarks/experiment-data"])
# parser.add_argument('--exp_json_path', default="configs/exp_setup.json")
parser.add_argument("--sancov_util_results_path", default="./scripts/sancov_util_results")
parser.add_argument("--foreign", default=False)
args = vars( parser.parse_args())
results_path = args['sancov_util_results_path'
]
FOREIGN = args['foreign']
# bench_json = get_exp_json(args['exp_json_path'])
# BENCHMARKS, FLAGS = bench_json['benchmarks'], bench_json['flags']
out = open("out/unique_edges_compare.csv", 'a+')
CSV_WRITER = csv.writer(out, delimiter=',')

out = open("out/unique_edges_total.csv", 'a+')
CSV_WRITER2 = csv.writer(out, delimiter=',')


handle_results(results_path)
# print(COVERED_EDGES.keys())
for fuzzer, benchmark in COVERED_EDGES.keys():
    total = COVERED_EDGES[(fuzzer,benchmark)]
    all = COVERED_EDGES[(fuzzer,benchmark)]
    for compare_to_fuzzer, compare_to_benchmark in COVERED_EDGES.keys():
        if(benchmark == compare_to_benchmark):
            diff = len(COVERED_EDGES[(fuzzer,benchmark)] - COVERED_EDGES[(compare_to_fuzzer,compare_to_benchmark)])
            row = [benchmark, fuzzer, compare_to_fuzzer, diff,len(all)]
            CSV_WRITER.writerow(row)
            if(fuzzer != compare_to_fuzzer):
                total =  total - COVERED_EDGES[(compare_to_fuzzer,compare_to_benchmark)]


    CSV_WRITER2.writerow([benchmark,fuzzer, len(total)])
            




out.close()
