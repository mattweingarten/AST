import sys
import os
import argparse
from argparse import ArgumentParser
import angr
from angrutils import * 


parser = ArgumentParser()


parser.add_argument('--binary', default="")



args = vars( parser.parse_args())

binary = args['binary']



proj = angr.Project(binary, auto_load_libs=False)
cfg = proj.analyses.CFGFast()
# entry_node = cfg.get_any_node(proj.entry)

# # main = proj.loader.main_object.get_symbol("main")




# plot_cfg(cfg, "ais3_cfg", asminst=True, remove_imports=True, remove_path_terminator=True)  

# print(cfg)    
print("nodes:" + str(len(cfg.graph.nodes())))
print("edges: " + str(len(cfg.graph.edges())))
# print(len(list(cfg.graph.successors(entry_node))))


# proj = angr.Project("/home/matt/bingraphvis/samples/cfg/cfg_0", load_options={'auto_load_libs':False})
# main = proj.loader.main_object.get_symbol("main")
# start_state = proj.factory.blank_state(addr=main.rebased_addr)
# cfg = proj.analyses.CFGEmulated(fail_fast=True, starts=[main.rebased_addr], initial_state=start_state)
# plot_cfg(cfg, "test", asminst=True, remove_imports=True, remove_path_terminator=True)  