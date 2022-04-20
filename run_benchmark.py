from pickle import GLOBAL
import sys
import re
import os
import argparse

from argparse import ArgumentParser



COMMAND  = "PYTHONPATH=. python3 experiment/run_experiment.py --experiment-config {config}  --experiment-name {name} --benchmarks {benchmark}  --fuzzers {fuzzers}"  

parser = ArgumentParser()
parser.add_argument('--benchmarks', nargs='+', default=[])
parser.add_argument('--fuzzers', nargs='+', default=[])
parser.add_argument('--config', default="")
parser.add_argument('--n', default=1)
args = vars( parser.parse_args())

# fuzzers = " ".join(args['fuzzers'])

for benchmark in args['benchmarks']:
    for fuzzer in args['fuzzers']:
        name = benchmark + "-" +  fuzzer
        name =  re.sub("[^0-9a-z-]+", "", name)
        name = name[:28] + str(args['n'])
        os.system(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzer,config=args['config']))
    # print(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzers,config=args['config']))





