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
parser.add_argument('--n', default="1")
args = vars( parser.parse_args())

# fuzzers = " ".join(args['fuzzers'])

# for benchmark in args['benchmarks']:
#     for fuzzer in args['fuzzers']:
#         name = benchmark + "-" +  fuzzer
#         name =  re.sub("[^0-9a-z-]+", "", name)
#         name = name[:28] + str(args['n'])
#         os.system(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzer,config=args['config']))
#     # print(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzers,config=args['config']))


for benchmark in args['benchmarks']:
    name = benchmark + '_' + args['n']
    name =  re.sub("[^0-9a-z-]+", "", name)
    fuzzers = " ".join(args['fuzzers'])
    os.system(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzers,config=args['config']))
    # print(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzers,config=args['config']))
    # for fuzzer in args['fuzzers']:
    #     name = benchmark + "-" +  fuzzer
    #     name =  re.sub("[^0-9a-z-]+", "", name)
    #     name = name[:28] + str(args['n'])
    # print(COMMAND.format(name=name,benchmark=benchmark,fuzzers=fuzzers,config=args['config']))


# python3 ../AST/run_benchmark.py --benchmarks lcms-2017-03-21 bloaty_fuzz_target libxml2-v2.9.2  --fuzzers aflplusplus_ast_o0 aflplusplus_ast_o1 aflplusplus_ast_o2 aflplusplus_ast_o3 aflplusplus_ast_f0 aflplusplus_ast_f1 --n f_o_all_2 --config ../AST/wmatt/experiment-config.yaml


