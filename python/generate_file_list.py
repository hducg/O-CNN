# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:43:49 2019

@author: 2624224
"""

import argparse
import os

def names_file_from_dir(rootdir, subdir, suffix = ''):
    file_dir = rootdir + subdir
    
    list_name = file_dir + '_names.txt'
    
    file_names = os.listdir(file_dir)
    
    with open(list_name, 'w') as f:
        for name in file_names:
            if suffix is not '' and name.find(suffix) is not -1:
                f.write(subdir + '/' + name + '\n')

            
def paths_file_from_dir(rootdir, subdir):
    
    file_dir = rootdir + subdir
    
    list_name = file_dir + '_paths.txt'
    
    file_names = os.listdir(file_dir)
    
    with open(list_name, 'w') as f:
        for name in file_names:
            f.write(file_dir + '/' +name + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--rootdir",
                        type=str,
                        help="Base folder containing the directory of files. Example: F:/wjcao/datasets/TestCAD/",
                        required=True)
    
    parser.add_argument("--subdir",
                        type=str,
                        help="name of the sub-directory containing the files. Example: test_cad_octree_6",
                        required=True)
    
    args = parser.parse_args()

    names_file_from_dir(args.rootdir, args.subdir)
    paths_file_from_dir(args.rootdir, args.subdir)    
            