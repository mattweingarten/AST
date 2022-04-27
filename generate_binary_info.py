#see https://docs.angr.io/introductory-errata/install to install angr for binary analysis

#requires binary to contain the name of the benchmark as in benchmarks.json contain the name of a flag.
#Flags can be passed (or default to all o0-o3)



import json
import sys
import os
import argparse
from argparse import ArgumentParser
import angr
from angrutils import * 
import csv


def isElf(file):
    f = open(file,'rb')
    l = f.readline()
    if(l[1] == 69 and l[2] == 76 and l[3] == 70): #check executable
       f.close()
       return True
    else:
        f.close()
        return False 

def get_benchmark(f, benchmarks):
    for benchmark in benchmarks:
        if benchmark in f:
            return benchmark

def get_flag(f, flags):
    for flag in flags:
        if flag in f:
            return flag


def binary_analysis(elf): #returns (nodes,edges)
    proj = angr.Project(elf, auto_load_libs=False)
    cfg = proj.analyses.CFGFast()
    return len(cfg.graph.nodes()), len(cfg.graph.edges())

def handle_folder(curr_dir, flags, benchmarks,csv_writer):
    all_files = [f for f in os.scandir(curr_dir)]
    folders = [f.path for f in  all_files if f.is_dir() and not 'src' in  f.path]
    elfs = [f.path for f in  all_files if not f.is_dir() and isElf(f)]
    
    if(len(elfs) > 0):
        

        for elf in elfs:
            flag = get_flag(elf,flags)
            benchmark = get_benchmark(elf,benchmarks)
            print("Doing analysis on elf: " + elf + "...")
            nodes,edges = binary_analysis(elf)
            # nodes,edges = (0,0)
            csv_writer.writerows([[benchmark,flag,str(nodes),str(edges)]])



    [ f.path for f in os.scandir(starting_dir) if f.is_dir() ]


    
    for folder in folders: 
        handle_folder(folder, flags, benchmarks, csv_writer)



# Main
parser = ArgumentParser()


parser.add_argument('--folder', default="")


parser.add_argument('--flags',nargs='+', default=["o0", "o1", "o2", "o3"], required=False)

args = vars( parser.parse_args())


bench_file = open("benchmarks.json")

bench_json = json.load(bench_file)



data_f = open("binary_data.csv", 'a+')
csv_writer = csv.writer(data_f, delimiter=',')
starting_dir = args['folder']
flags = args['flags']
handle_folder(starting_dir, flags, bench_json['benchmarks'],csv_writer)

bench_file.close()
data_f.close()




