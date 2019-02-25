# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 17:26:25 2019

@author: 2624224
"""
import os
import subprocess
import shutil

caffe = 'C:/Users/2624224/caffe/build/tools/Release/caffe.exe'

dataset_dir = 'C:/Users/2624224/caffe/data/shapenet/'
category = '03001627'

feature_dir = dataset_dir + category + '_feature/'
if not os.path.exists(feature_dir):
	os.mkdir(feature_dir)

# modify prototxt specified by --model: data source; num_output of deconv2_ip layer
# set --weights to the right trained caffemoddel  
# set --iterations to the number of models to be tested	
blob_prefix = '--blob_prefix=' + feature_dir
subprocess.check_call([caffe, 'test', '--model=C:/Users/2624224/caffe/examples/o-cnn/segmentation_5_test.prototxt', '--weights=C:/Users/2624224/caffe/examples/o-cnn/seg_5.caffemodel', 
'--gpu=0', blob_prefix, '--binary_mode=false', '--save_seperately=true', '--iterations=749'])