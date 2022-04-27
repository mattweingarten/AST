from shutil import copytree
import sys
import re
import os
from distutils.dir_util import copy_tree


def base(path):
    return os.path.basename(os.path.normpath(path))

if(len(sys.argv) < 3):
    print("Pass from and to directory please")
    exit(1)


from_dir = sys.argv[1]
to_dir = sys.argv[2]
subfolders = [ f.path for f in os.scandir(from_dir) if f.is_dir() ]


for f in subfolders: 
    base_path = base(f)
    new = os.path.join(to_dir, base_path)
    os.mkdir(new)

    input_dir = os.path.join(f, 'input')
    coverage_dir = os.path.join(f,'coverage')
    
    copy_tree(input_dir,new)
    copy_tree(coverage_dir,new)
