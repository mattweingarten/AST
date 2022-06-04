#see https://docs.angr.io/introductory-errata/install to install angr for binary analysis

#requires binary to contain the name of the benchmark as in benchmarks.json contain the name of a flag.
#Flags can be passed (or default to all o0-o3)



import json
import sys
import os
import argparse
from argparse import ArgumentParser
# import angr
# from angrutils import * 
import csv
from util import *
from util import get_exp_json
import subprocess



# def binary_analysis(elf): #returns (nodes,edges)
#     proj = angr.Project(elf, auto_load_libs=False)
#     cfg = proj.analyses.CFGFast()
#     return len(cfg.graph.nodes()), len(cfg.graph.edges())

def handle_folder(curr_dir, flags, benchmarks,csv_writer):
    all_files = [f for f in os.scandir(curr_dir)]
    folders = [f.path for f in  all_files if f.is_dir() and not 'src' in  f.path]
    elfs = [f.path for f in  all_files if not f.is_dir() and isElf(f)]
    
    if(len(elfs) > 0):
        
        p = list()
        for elf in elfs:
            # flag = get_flag(elf,flags)
            # benchmark = get_benchmark(elf,benchmarks)
            # print("Doing analysis on elf: " + elf + "...")
            # nodes,edges = binary_analysis(elf)
            # # nodes,edges = (0,0)
            # csv_writer.writerows([[benchmark,flag,str(nodes),str(edges)]])
            command = [
                "python3",
                "./scripts/handle_single_binary.py",
                elf,
                get_flag(elf,flags),
                get_benchmark(elf, benchmarks)
            ]
            print(command)
            sub = subprocess.Popen(command)
            sub.wait()
        
        # exit_codes = [x.wait() for x in p]




    [ f.path for f in os.scandir(starting_dir) if f.is_dir() ]


    
    for folder in folders: 
        handle_folder(folder, flags, benchmarks, csv_writer)



# Main
parser = ArgumentParser()


parser.add_argument('--folder', default="")
parser.add_argument('--exp_json_path', default="configs/exp_setup.json")

args = vars( parser.parse_args())



bench_json = get_exp_json(args['exp_json_path'])



out = open("out/binary_data.csv", 'a+')
csv_writer = csv.writer(out, delimiter=',')
starting_dir = args['folder']
handle_folder(starting_dir, bench_json['flags'], bench_json['benchmarks'],csv_writer)

out.close()




