# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 17:26:25 2019

@author: 2624224
"""
import os
import subprocess
import shutil

caffe = 'C:/Users/2624224/caffe/build/tools/Release/caffe.exe'

dataset_dir = 'C:/Users/2624224/caffe/data/cad/'
category = 'test'

feature_dir = dataset_dir + category + '_feature/'
if not os.path.exists(feature_dir):
	os.mkdir(feature_dir)
	
blob_prefix = '--blob_prefix=' + feature_dir
subprocess.check_call([caffe, 'test', '--model=C:/Users/2624224/caffe/examples/o-cnn/segmentation_6_test.prototxt', '--weights=C:/Users/2624224/caffe/examples/o-cnn/seg_6_cad.caffemodel', 
'--gpu=0', blob_prefix, '--binary_mode=false', '--save_seperately=true', '--iterations=43'])