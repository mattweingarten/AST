from argparse import ArgumentParser
from ast import arg
from util import * 
import os
import csv
import sys

def handle_exp(exp):
    runs = [f.path for f in os.scandir(exp) if f.is_dir()]
    for run in runs:
        try:
            handle_data(os.path.join(run,"data"))
        except: 
            try: 
                handle_data(os.path.join(run,"coverage","data"))
            except Exception as e:
                print(e)
                print("Couldnt parse data.." + run)

def handle_data(data):
    bs = [f.path for f in os.scandir(data) if f.is_dir()]
    for b in bs: 
        handle_trial(b) 
    
def handle_trial(trial):
    bench_flag_pairs = [f.path for f in os.scandir(trial) if f.is_dir()]
    bf_pairs = [(get_benchmark(b_f_pair,BENCHMARKS),get_flag(b_f_pair,FLAGS)) for b_f_pair in bench_flag_pairs]
    covered_regions_dict = {}
    for b_f_pair in bench_flag_pairs:
        bench,flag = bench,flag = get_benchmark(b_f_pair,BENCHMARKS),get_flag(b_f_pair,FLAGS)
        cov = get_exp_json(b_f_pair + "/covered_regions.json")
        cov_set = set()
        for region in cov:
            cov_set.add(tuple(region))
        covered_regions_dict[concat(bench,flag)] = cov_set


    for (l_b,l_f) in bf_pairs:
        for (r_b,r_f) in bf_pairs:
            diff = get_num_regions_without((l_b,l_f),(r_b,r_f),covered_regions_dict)
            CSV_WRITER.writerow([l_b,l_f,r_b,r_f, diff])

    
def get_num_regions_without(bf1,bf2,covered_regions_dict):
    return len(covered_regions_dict[bf1] - covered_regions_dict[bf2])



def read_sancov(f):
    print(f)
    f_d = open(f,'r')
    edges = set()
    for line in f_d:
        edges.add(int(line, 16))
    f_d.close()
    return edges



def handle_bench_flag_pair(bench, flag, dir):
    edges = set()
    for trial in  [f.path for f in os.scandir(dir) if f.is_dir()]:
        edges = edges.union(read_sancov(trial + '/sancov_out.txt'))
    return edges


# def handle_exp(bench, dir):


# def diff(a, b):
#     res = set()
#     return res.union(a - b).union(b - a)

# #Main
# parser = ArgumentParser()

# bench_json = get_exp_json(args['exp_json_path'])
# BENCHMARKS, FLAGS = bench_json['benchmarks'], bench_json['flags']
# # parser.add_argument('--exp_folders',nargs='+', default=["wmatt/experiment-data", "bean/benchmarks/experiment-data"])
# parser.add_argument('--exp_json_path', default="configs/exp_setup.json")

# args = vars( parser.parse_args())
# out = open("out/unique_region.csv", 'a+')
# CSV_WRITER = csv.writer(out, delimiter=',')

# for exp in args['exp_folders']:
#     handle_exp(exp)

# edges1 = read_sancov(sys.argv[1])
# # edges2 = read_sancov(sys.argv[2])
# e = handle_bench_flag_pair('b','f',sys.argv[1])
# print(e)
# diff1 = diff(edges1, edges2)
# print(len(diff1))
