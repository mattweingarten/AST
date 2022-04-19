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
args = vars( parser.parse_args())

fuzzers = " ".join(args['fuzzers'])

for benchmark in args['benchmarks']:
    name = benchmark + "-"  +  fuzzers.replace(" ", "-")
    name =  re.sub("[^0-9a-z-]+", "", name)
    name = name[:29]
    os.system(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzers,config=args['config']))
    # print(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzers,config=args['config']))





