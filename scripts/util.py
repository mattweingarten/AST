import json
import os.path

def cut_fuzz_name(name):
    if(name == "afl_from_input_seed"):
        return "O2 + O3"
    if("native" in name):
        return "O3_native"
    if("disable" in name):
        return "O0_lto"
    return name[12:]

def isElf(file):
    f = open(file,'rb')
    l = f.readline()
    try:
        if(l[1] == 69 and l[2] == 76 and l[3] == 70): #check executable
           f.close()
           return True
    except:
        pass
    f.close()
    return False

def get_benchmark(file, benchmarks):
    print(file, benchmarks)
    for benchmark in benchmarks:
        if benchmark in file:
            return benchmark


def get_flag(file, flags):
    if ("aflplusplus_ast_o3_lto") in file:
        return "aflplusplus_ast_o3_lto"
    if("aflplusplus_ast_o0_lto" in file):
        return "aflplusplus_ast_o3_lto"
    if("aflplusplus_ast_o3_native" in file):
        return "aflplusplus_ast_o3_native"
    for flag in flags:
        if flag in file:
            return flag

def concat(bench,flag):
    return (bench,flag)


def get_exp_json(path):
    exp_file = open(path)
    exp_json = json.load(exp_file)
    return exp_json

