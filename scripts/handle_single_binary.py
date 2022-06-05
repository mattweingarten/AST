import json
import sys
import os
import argparse
from argparse import ArgumentParser
import angr
from angrutils import * 
import csv
from util import *
from util import get_exp_json
import subprocess
import sys





def binary_analysis(elf): #returns (nodes,edges)
    proj = angr.Project(elf, auto_load_libs=False)
    cfg = proj.analyses.CFGFast()
    # return 0,0
    return len(cfg.graph.nodes()), len(cfg.graph.edges())

def main():
    out = open("out/binary_data." + str(os.getpid()) + ".csv", 'a+')
    csv_writer = csv.writer(out, delimiter=',')

    elf = sys.argv[1]
    flag = sys.argv[2]
    benchmark = sys.argv[3]
    print("Doing analysis on elf: " + elf + "...")
    nodes,edges = binary_analysis(elf)
    # nodes,edges = (0,0)
    csv_writer.writerows([[benchmark,flag,str(nodes),str(edges)]])
    out.close()

if __name__ == "__main__":
    main()
    