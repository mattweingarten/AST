from argparse import ArgumentParser
from util import * 
import os
import csv


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

#Main
parser = ArgumentParser()
parser.add_argument('--exp_folders',nargs='+', default=["wmatt/experiment-data", "bean/benchmarks/experiment-data"])
parser.add_argument('--exp_json_path', default="configs/exp_setup.json")

args = vars( parser.parse_args())

bench_json = get_exp_json(args['exp_json_path'])
BENCHMARKS, FLAGS = bench_json['benchmarks'], bench_json['flags']
out = open("out/unique_region.csv", 'a+')
CSV_WRITER = csv.writer(out, delimiter=',')

for exp in args['exp_folders']:
    handle_exp(exp)




out.close()
