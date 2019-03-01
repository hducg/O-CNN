# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 16:24:02 2019

@author: 2624224
"""
import pickle
import os

from data_import_export import shape_with_fid_to_step, shape_with_fid_from_step, upgraded_point_cloud_to_file, labels_from_file, label_index_from_file        
from model_factory import shape_drain
from point_cloud import point_cloud_from_labeled_shape 

root_dir = 'F:/wjcao/datasets/TestCAD/'
category_name = 'marche'
num_shapes = 3

shape_dir = root_dir + category_name + '_shape/'
points_dir = root_dir + category_name + '_points/'
octree_dir = root_dir + category_name + '_octree/'
lmdb_dir = root_dir + category_name + '_lmdb/'
feature_dir = root_dir + category_name + '_feature/'
list_dir = root_dir + category_name + '_list/'

path_names = [shape_dir, points_dir, octree_dir, feature_dir, list_dir]
for path in path_names:
    if not os.path.exists(path):
        os.mkdir(path)

def generate_paths_file(where, to, suffix):    
    prefix = where
    if suffix is 'octree':
        prefix = where.split('/')[-2] + '/'

    names = os.listdir(where)
    
    filename = category_name + '_' + suffix + '.txt'
    print(filename)
    filepath = to + filename
    with open(filepath, 'w') as f:
        for name in names:
            if suffix is not '' and name.find(suffix) is not -1:
                f.write(prefix + name + '\n')
    
                
def generate_shapes():    
    for i in range(num_shapes):
        shape, label_map, id_map, shape_name = shape_drain()
        
        step_path = shape_dir + shape_name + '.step'
        shape_with_fid_to_step(step_path, shape, id_map)
        
        face_truth_path = shape_dir + shape_name + '.face_truth'
        face_truth = [label_map[f] for f, fid in sorted(id_map.items(), key = lambda kv: kv[1])]    
        with open(face_truth_path, 'wb') as f:
            pickle.dump(face_truth, f)

        
def generate_points():
    shape_list_dir = list_dir + category_name + '_step.txt'
    with open(shape_list_dir) as f:
        shape_dirs = [line.strip() for line in f.readlines()]

    for path in shape_dirs:
        shape, id_map = shape_with_fid_from_step(path)
        shape_name = path.split('/')[-1].split('.')[0]

        face_truth_path = shape_dir + shape_name + '.face_truth'
        with open(face_truth_path, 'rb') as f:
            face_truth = pickle.load(f)        
        label_map = {f: face_truth[id_map[f]] for f in id_map}
                     
        pts, normals, segs, face_ids = point_cloud_from_labeled_shape(shape, label_map, id_map)
        file_path = points_dir + shape_name + '.points'
        upgraded_point_cloud_to_file(file_path,pts,normals,[],segs)
        
        face_index_path = points_dir + shape_name + '.face_index'
        with open(face_index_path, 'wb') as f:
            pickle.dump(face_ids, f)
            
       
if __name__ == '__main__':
#1. shape_drain --> shape, label_map, id_map, shape_name    
#    generate_shapes()
#    generate_paths_file(shape_dir, list_dir, 'step')    

#2. shape, label_map, id_map --> point_cloud.py --> *.points, *.face_index, *.points_truth    
    generate_points()
    generate_paths_file(points_dir, list_dir, 'points')
    

    

