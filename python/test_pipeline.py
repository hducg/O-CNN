# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 16:24:02 2019

@author: 2624224
"""
import pickle
import os
import subprocess
import operator

from data_import_export import shape_with_fid_to_step, shape_with_fid_from_step, point_cloud_to_file, labels_from_file, label_index_from_file        
from model_factory import shape_drain
from point_cloud import point_cloud_from_labeled_shape 

root_dir = 'F:/wjcao/datasets/TestCAD/'
category_name = 'lundi'
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
    shape_list_dir = list_dir + category_name + '_shape.txt'
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
        point_cloud_to_file(file_path,pts,normals,segs)
        
        face_index_path = points_dir + shape_name + '.face_index'
        with open(face_index_path, 'wb') as f:
            pickle.dump(face_ids, f)
            

def generate_label_files():
    octree_list_path = list_dir + category_name + '_octree.txt'
    f = open(octree_list_path, 'r')
    lines = f.readlines()
    f.close()
        
    labels_names = os.listdir(feature_dir)
    
    depth_sep = lines[0].partition('upgrade')[2].split('.')[0] 
    print(depth_sep)
    
    for i in range(len(lines)):
        shape_name = lines[i].split('/')[1].split('.')[0]
    
        labels_path = feature_dir + labels_names[2 * i + 1]
        print(labels_path)
        labels = labels_from_file(labels_path)
    
        label_index_path = octree_dir + shape_name + '.upgrade' + depth_sep + '.label_index'
        print(label_index_path)
        label_index = label_index_from_file(label_index_path)
    
        points_predicted = [labels[index] for index in label_index]
        points_predicted_path = points_dir + shape_name + depth_sep + '.points_predicted'
        print(points_predicted_path)
        with open(points_predicted_path, 'wb') as f:
            pickle.dump(points_predicted, f)
    
    # to be debugged        
        face_index_path = points_dir + shape_name + '.face_index'
        with open(face_index_path, 'rb') as f:
            face_index = pickle.load(f)
    
        face_label_map = {}
        for i in range(len(points_predicted)):
            fid = face_index[i]
            label = points_predicted[i]
            if fid not in face_label_map:
                face_label_map[fid] = {label:1}
            else:
                if label in face_label_map[fid]:
                    face_label_map[fid][label] += 1
                else:
                    face_label_map[fid][label] = 1
    
        face_predicted = [max(face_label_map[key].items(), key = operator.itemgetter(1))[0] for key in sorted(face_label_map.keys())]
        face_predicted_path = shape_dir + shape_name + '.face_predicted'
        with open(face_predicted_path, 'wb') as f:
            pickle.dump(face_predicted, f)
                
        
upgrade_points = 'F:/wjcao/github/hducg/O-CNN/ocnn/octree/build/Release/upgrade_points.exe'
octree = 'F:/wjcao/github/hducg/O-CNN/ocnn/octree/build/Release/octree.exe'
convert_octree_data = ''
caffe = ''
if __name__ == '__main__':
#1. shape_drain --> shape, label_map, id_map, shape_name    
#    generate_shapes()
#    generate_paths_file(shape_dir, list_dir, 'step')    

#2. shape, label_map, id_map --> point_cloud.py --> *.points, *.face_index, *.points_truth    
#    generate_points()
#    generate_paths_file(points_dir, list_dir, 'points')
    
#3. filenames, output_path --> upgrade_points.py --> *.upgrade.points
#    points_list = list_dir + category_name + '_points.txt'
#    subprocess.check_call([upgrade_points, '--filenames', points_list, '--output_path', points_dir])
#    generate_paths_file(points_dir, list_dir, 'upgrade.points')
    
#4. filenames, output_path --> octree.exe --> *.octree, *.label_index
#    upgrade_list = list_dir + category_name + '_upgrade.points.txt'
#    subprocess.check_call([octree, '--filenames', upgrade_list, '--output_path', octree_dir, '--depth', '6', '--rot_num', '1'])
#    generate_paths_file(octree_dir, list_dir, 'octree')
#5. rootfolder, listfile, db_name --> convert_octree_data --> lmdb, octree_list_name
    if os.path.exists(lmdb_dir):
        os.remove(lmdb_dir)
    octree_list = list_dir + category_name + '_octree.txt'
    subprocess.check_call([convert_octree_data, root_dir, octree_list, lmdb_dir])
#6. prototxt, caffemodel --> caffe test --> *.label_groundtruth, *.label_predicted
    blob_prefix = feature_dir
    model_path = ''
    weights_path = ''        
    subprocess.check_call([caffe, 'test', '--model=' + model_path, '--weights=' + weights_path, '--gpu=0', '--blob_prefix=' + blob_prefix, 
    '--binary_mode=false', '--save_seperately=true', '--iterations=' + str(num_shapes)])    
#7. generate label files
    generate_label_files()
