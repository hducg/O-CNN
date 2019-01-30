# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 09:56:49 2019

@author: 2624224
"""

dataset_dir = 'F:/wjcao/datasets/TestCAD/'

upgrade_points = 'F:/wjcao/github/O-CNN/ocnn/octree/build/Release/upgrade_points.exe'

import os
import subprocess

def filenames_from_dir(file_dir):
    names = []
    for root,_,filenames in os.walk(file_dir):
        names += filenames
        
    return names

def prepare_octree_from_points(category_name):        
    points_dir = dataset_dir + category_name
    print(points_dir)
    upgraded_points_dir = points_dir + '_upgraded'
    print(upgraded_points_dir)
    upgraded_octree_dir = points_dir + '_octree'
    print(upgraded_octree_dir)

    points_names = filenames_from_dir(points_dir)    
        
    # 0. generate model list
    model_names = [name.split('.')[0] + '\n' for name in points_names]
    print(model_names)
    model_list_file = points_dir + '_model_list.txt'
    with open(model_list_file, 'w') as f:
        f.writelines(model_names)
    
    # 1. generate points list
    points_paths =[points_dir + '/' + name + '\n' for name in points_names]
    points_file = points_dir + '_points_list.txt'
    with open(points_file, 'w') as f:
        f.writelines(points_paths)
            
    # 2. upgrade points
    subprocess.check_call([upgrade_points, '--filenames', points_file, '--output_path', upgraded_points_dir])
    
    # 3. generate upgraded points list
    points_names = filenames_from_dir(upgraded_points_dir)
    points_paths = [upgraded_points_dir + '/' + name + '\n' for name in points_names]
    points_file = upgraded_points_dir + '_list.txt'
    with open(points_file, 'w') as f:
        f.writelines(points_paths)
        
        
rocket = '04099429'        
#prepare_octree_from_points(rocket)
prepare_octree_from_points('test')
#prepare_octree_from_points('train')