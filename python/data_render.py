# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 17:05:26 2019

@author: 2624224
"""

from OCC.AIS import AIS_PointCloud, AIS_ColoredShape
from OCC.Graphic3d import Graphic3d_ArrayOfPoints
from OCC.Display.OCCViewer import rgb_color
from OCC.Display.SimpleGui import init_display

import os
import random
import pickle

from data_import_export import upgraded_point_cloud_from_file, labels_from_file, label_index_from_file, shape_with_fid_from_step


colors = [rgb_color(0,0,0), rgb_color(0.75,0.75,0.75), rgb_color(1,0,0), rgb_color(1,0.5,0), 
          rgb_color(0,1,1), rgb_color(1,0,1), rgb_color(1,0.8,0.8), rgb_color(1,1,0.8), 
          rgb_color(0.8,1,1), rgb_color(1,0.8,1), rgb_color(0.4,0,0), rgb_color(0.4,0.4,0), 
          rgb_color(0,0.4,0.4), rgb_color(0.4,0,0.4)]


class SegShapeViewer:
    '''
    input
        octree_list_file_name: 
            content example: test_octree/hole-1(1[triangle2])3(2[sweep]1[circle])2(2[sweep])4(1[circle]2[sweep]1[rectangle]).upgrade_6_2_000.octree
        dataset_dir: direcotry where directories of points, octrees and labels are
            example: 'F:/wjcao/datasets/TestCAD'
            points directory example: test_upgraded, octree directory example: test_octree      
    '''
    def __init__(self, root_path, category_name, list_name, depth_sep):
        self.shape_points_mode = 'shape'
        self.truth_predicted_mode = 'truth'
        self.depth_sep = depth_sep
        self.dataset_dir = root_path                
        self.points_category = category_name
        self.current_index = 0
        
        list_path = root_path + '/' + category_name + '_list/' + list_name
        f = open(list_path, 'r')
        lines = f.readlines()
        f.close()
        
        # list of points names, example: hole-1(1[triangle2])3(2[sweep]1[circle])2(2[sweep])4(1[circle]2[sweep]1[rectangle]).upgrade
        self.shape_names = []
        # list of points category names, same length as shape_names, example: test
        
        
        for line in lines:
            # string specific to octree file names, example: _6_2_000            
            self.shape_names.append(line.split('/')[-1].split('.')[0])            
             

    def load_shape(self):
        
        # load shape and face_index
        shape_path = self.dataset_dir + '/' + self.points_category + '_shape/' + self.shape_names[self.current_index] + '.step'
        self.shape, id_map = shape_with_fid_from_step(shape_path)
        face_truth_path = self.dataset_dir + '/' + self.points_category + '_shape/' + self.shape_names[self.current_index] + '.face_truth'
        with open(face_truth_path, 'rb') as f:
            label_map = pickle.load(f)
        self.face_truth = {f:label_map[id_map[f]] for f in id_map}

        face_predicted_path = self.dataset_dir + '/' + self.points_category + '_shape/' + self.shape_names[self.current_index] + '.face_predicted'
        if os.path.exists(face_predicted_path):
            with open(face_predicted_path, 'rb') as f:
                label_map = pickle.load(f)
            self.face_predicted = {f:label_map[id_map[f]] for f in id_map}

        # load point cloud        
        points_path = self.dataset_dir + '/' + self.points_category + '_points/' + self.shape_names[self.current_index] + '.points'
        self.points,normals,features,self.points_truth = upgraded_point_cloud_from_file(points_path)
        
        points_predicted_path = self.dataset_dir + '/' + self.points_category + '_points/' + self.shape_names[self.current_index] + self.depth_sep + '.points_predicted'
        if os.path.exists(points_predicted_path):
            with open(points_predicted_path, 'rb') as f:
                self.points_predicted = pickle.load(f)        
        
                 
    def next_shape(self):
        self.current_index += 1
        if self.current_index >= len(self.shape_names):
            self.current_index = 0
            
        print(self.shape_names[self.current_index])
        self.load_shape()
        self.display()
            
    
    def display(self):
        if self.shape_points_mode is 'shape':
            if self.truth_predicted_mode is 'truth':
                display_shape(self.shape, self.face_truth)
                self.label_suffix = 'shape_groundtruth'
            else:
                display_shape(self.shape, self.face_predicted)
                self.label_suffix = 'shape_predicted'
        else:
            if self.truth_predicted_mode is 'truth':
                display_points(self.points, self.points_truth)
                self.label_suffix = 'points_groundtruth'
            else:
                display_points(self.points, self.points_predicted)
                self.label_suffix = 'points_predicted'
                      
        
    def save_image(self):
        image_name = self.dataset_dir + '/' + self.points_category + '_feature/' + self.shape_names[self.current_index] + self.label_suffix + '.jpeg'
        occ_display.View.Dump(image_name)
              
        
def display_shape(shape, fmap):
    occ_display.EraseAll()
    ais = AIS_ColoredShape(shape)    
    for f in fmap:        
        ais.SetCustomColor(f, colors[fmap[f]])    
    
    occ_display.Context.Display(ais.GetHandle())
    occ_display.View_Iso()
    occ_display.FitAll()
    
    
def display_points(pts, labels):
    occ_display.EraseAll() 
    
    print('number of points:', len(pts))
    feats = [None] * 14

    if len(labels) > 0:
        for i in range(len(pts)):
            feat_id = labels[i]
            if feats[feat_id] is None:
                feats[feat_id] = [pts[i]]
            else:
                feats[feat_id].append(pts[i])
    else:
        feats[0] = pts
                                
    for i in range(len(feats)):
        feat = feats[i]
        if feat is None:
            continue                        
        print('number of feature ' + str(i) + ' points:', len(feat))
        n_points = len(feat)
        points_3d = Graphic3d_ArrayOfPoints(n_points)
        for pt in feat:
            points_3d.AddVertex(pt[0], pt[1], pt[2])
    
        point_cloud = AIS_PointCloud()
        point_cloud.SetPoints(points_3d.GetHandle())
        point_cloud.SetColor(colors[i])
    
        ais_context.Display(point_cloud.GetHandle())  
    occ_display.View_Iso()
    occ_display.FitAll()

            
occ_display, start_occ_display, add_menu, add_function_to_menu = init_display()
ais_context = occ_display.GetContext().GetObject()

#category_names = ['03001627','04099429','03790512','03797390']
#dataset_dir = 'F:/wjcao/datasets/ocnn'
#labels_subdir = category_names[0] + '_feature' 
#octree_list_file_name = dataset_dir + category_names[0] + '_octree_names_shuffle.txt'


root_path = 'D:/Weijuan/dataset/cad'
category_name = 'marche'
list_name = 'marche_step.txt'
depth_sep = '_6_2_000'

points_render = SegShapeViewer(root_path, category_name, list_name, depth_sep)

def next_shape():
    points_render.next_shape()

        
def save_image():
    points_render.save_image()

    
def save_all():
    for i in range(min(len(points_render.shape_names),50)):
        points_render.next_shape()
        save_image()
        points_render.display_predicted()
        save_image()
                
        
def switch_shape_points():
    if points_render.shape_points_mode is 'shape':        
        points_render.shape_points_mode = 'points'
        points_render.display()
    else:
        points_render.shape_points_mode = 'shape'
        points_render.display()

        
def switch_truth_predicted():
    if points_render.truth_predicted_mode is 'predicted':
        points_render.truth_predicted_mode = 'truth'
        points_render.display()
    else:
        points_render.truth_predicted_mode = 'predicted'
        points_render.display()
        
if __name__ == '__main__':
    random.seed()
           
    add_menu('Display')
    add_function_to_menu('Display', next_shape)
    add_function_to_menu('Display', switch_shape_points)
    add_function_to_menu('Display', switch_truth_predicted)
    add_function_to_menu('Display', save_image)
    add_function_to_menu('Display', save_all)    
    
    start_occ_display()
