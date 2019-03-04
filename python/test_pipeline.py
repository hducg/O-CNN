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

root_dir = 'D:/Weijuan/dataset/cad/'
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


def generate_label_files():
    octree_list_path = list_dir + category_name + '_octree_shuffle.txt'
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
                
        
octree = 'D:/Weijuan/O-CNN/ocnn/octree/build/Release/octree.exe'
convert_octree_data = 'D:/Weijuan/caffe/build/tools/Release/convert_octree_data.exe'
caffe = 'D:/Weijuan/caffe/build/tools/Release/caffe.exe'
if __name__ == '__main__':   
#1. filenames, output_path --> octree.exe --> *.octree, *.label_index
    points_list = list_dir + category_name + '_.points.txt'
    subprocess.check_call([octree, '--filenames', points_list, '--output_path', octree_dir, '--depth', '6', '--rot_num', '1'])
    generate_paths_file(octree_dir, list_dir, 'octree')
#2. rootfolder, listfile, db_name --> convert_octree_data --> lmdb, octree_list_name
    if os.path.exists(lmdb_dir):
        os.remove(lmdb_dir)
    octree_list = list_dir + category_name + '_octree.txt'
    subprocess.check_call([convert_octree_data, root_dir, octree_list, lmdb_dir])
#3. prototxt, caffemodel --> caffe test --> *.label_groundtruth, *.label_predicted
    blob_prefix = feature_dir
    model_path = 'D:/Weijuan/caffe/examples/o-cnn/segmentation_6_test.prototxt'
    weights_path = 'D:/Weijuan/caffe/examples/o-cnn/seg_6_cad.caffemodel'        
    subprocess.check_call([caffe, 'test', '--model=' + model_path, '--weights=' + weights_path, '--gpu=0', '--blob_prefix=' + blob_prefix, 
    '--binary_mode=false', '--save_seperately=true', '--iterations=' + str(num_shapes)])    
#4. generate label files
    generate_label_files()
