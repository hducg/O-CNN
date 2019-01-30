# data preparation routine of TestCAD for caffe testing

dataset_dir = 'F:/wjcao/datasets/TestCAD/'
category = 'test'

octree = 'F:/wjcao/github/O-CNN/ocnn/octree/build/Release/octree.exe'

import os
import subprocess

from generate_file_list import paths_file_from_dir, names_file_from_dir

# 1. generate points list file, absolute paths are needed, name = category + '_upgraded_list.txt'
paths_file_from_dir(dataset_dir, category + '_upgraded')
    
# 2. generate octree with label_index
octree_dir = dataset_dir + category + '_octree'
points_list_file_path = dataset_dir + category + '_upgraded_paths.txt'
if not os.path.exists(octree_dir):
    subprocess.check_call([octree, '--filenames', points_list_file_path, '--output_path', octree_dir, '--depth', '6', '--rot_num', '1'])

# 3. generate octree name file, no paths, file in dataset_dir
names_file_from_dir(dataset_dir, category + '_octree', 'octree')

# 4. convert octree to lmdb

# 5. modify prototxt

# 6. run caffe test

# 7. visualize result 