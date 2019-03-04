# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 12:17:14 2019

@author: 2624224
"""

'''
input
    filename:   ''
    has_label:  bool
output
    pts:        [[float,float,float]]
    normals:    [[float,float,float]]
    segs：       [int]
'''    
import struct    
def point_cloud_from_file(filename, has_label=True):
    f = open(filename,'rb')
    num = struct.unpack('i', f.read(4))[0]
    print(num)
    pts = []
    for i in range(num):
        x = struct.unpack('f', f.read(4))[0]
        y = struct.unpack('f', f.read(4))[0]
        z = struct.unpack('f', f.read(4))[0]
        pts.append([x, y, z])        
    
    normals = []
    for i in range(num):
        x = struct.unpack('f', f.read(4))[0]
        y = struct.unpack('f', f.read(4))[0]
        z = struct.unpack('f', f.read(4))[0]
        normals.append([x, y, z])        
    
    segs = []
    if has_label is True:
        for i in range(num):
            seg = struct.unpack('i', f.read(4))[0]
            segs.append(seg)
    
    f.close()
    return pts, normals, segs
    

'''
input
    filename:   ''
    pts:        [[float,float,float]]
    normals:    [[float,float,float]]
    segs:       [int]    
'''    
def point_cloud_to_file(filename, pts, normals, segs):
    f = open(filename,'wb')
    num = len(pts)
    f.write(struct.pack('i',num))
    for p in pts:
        f.write(struct.pack('f',p[0]))
        f.write(struct.pack('f',p[1]))
        f.write(struct.pack('f',p[2]))
        
    for n in normals:
        f.write(struct.pack('f',n[0]))
        f.write(struct.pack('f',n[1]))
        f.write(struct.pack('f',n[2]))
        
    for s in segs:
        f.write(struct.pack('i',s))
        
    f.close() 
    
'''
input
    filename: ''
output
    pts:        [[float] * 3] * number of point
    normals:    [[float] * 3] * number of point
    features:   [[float] * number of channels] * number of point
    labels:     [int] * number of point
'''   
def upgraded_point_cloud_from_file(filename):
    f = open(filename,'rb')
        
    magic_str_ = []
    for i in range(16):
        magic_str_.append(struct.unpack('c',f.read(1))[0])
        
    npt = struct.unpack('i',f.read(4))[0]
    
    content_flags_ = struct.unpack('i',f.read(4))[0]
    
    channels_ = []
    for i in range(8):
        channels_.append(struct.unpack('i',f.read(4))[0])
        
    ptr_dis_ = []    
    for i in range(8):
        ptr_dis_.append(struct.unpack('i',f.read(4))[0])
    
    print(magic_str_)
    print(npt)
    print(content_flags_)
    print(channels_)
    print(ptr_dis_)
    
    pts = []    
    for i in range(npt):
        x = struct.unpack('f', f.read(4))[0]
        y = struct.unpack('f', f.read(4))[0]
        z = struct.unpack('f', f.read(4))[0]
        pts.append([x, y, z])
                    
    normals = []
    for i in range(npt):
        x = struct.unpack('f', f.read(4))[0]
        y = struct.unpack('f', f.read(4))[0]
        z = struct.unpack('f', f.read(4))[0]
        normals.append([x, y, z])
    
    features = []
    if content_flags_ & 4 != 0:
        cnum = channels_[2]
        for i in range(npt):
            feat = []
            for j in range(cnum):
                feat.append(struct.unpack('f',f.read(4))[0])
            features.append(feat)
            
    labels = [] 
    if content_flags_ & 8 != 0:
        for i in range(npt):
            label = struct.unpack('f',f.read(4))[0]
            labels.append(int(label))
    
    f.close()        
    return pts, normals, features, labels


def upgraded_point_cloud_to_file(filename, pts, normals, features, labels):
    print('upgraded_point_cloud_to_file')
    npt = len(pts)
    if len(normals) != npt and len(features) != npt:
        print('either normal or feature info is not correct')
        return npt
    
    f = open(filename, 'wb')
    magic_str = '_POINTS_1.0_\0\0\0\0'  
    for i in range(16):
        f.write(struct.pack('c', magic_str[i].encode('ascii')))
    
    f.write(struct.pack('i', npt))

    content_flags = 0|1 # KPoint = 1
    channels = [0] * 8
    channels[0] = 3   
    ptr_dis = [0] * 8    
    ptr_dis[0] = 88
    if len(normals) > 0:
        content_flags |= 2  # KNormal = 2
        channels[1] = 3
    if len(features) > 0:
        content_flags |= 4  # KFeature = 4
        channels[2] = len(features[0])
    if len(labels) > 0:
        content_flags |= 8  # KLabel = 8
        channels[3] = 1
    for i in range(1, 5):
        ptr_dis[i] = ptr_dis[i-1] + 4 * npt * channels[i-1]
        
    f.write(struct.pack('i', content_flags))
    
    for i in range(8):
        f.write(struct.pack('i', channels[i]))
        
    for i in range(8):
        f.write(struct.pack('i', ptr_dis[i]))
    
    for p in pts:
        f.write(struct.pack('f', p[0]))
        f.write(struct.pack('f', p[1]))
        f.write(struct.pack('f', p[2]))
    
    for n in normals:
        f.write(struct.pack('f', n[0]))        
        f.write(struct.pack('f', n[1]))
        f.write(struct.pack('f', n[2]))
    
    for f in features:
        for item in f:
            f.write(struct.pack('f', item))
            
    for l in labels:
        f.write(struct.pack('f',l))
        
    f.close()
    return npt
    
'''
input
    filename:   ''
output
    labels:     [int] * number of lines
'''    
def labels_from_file(filename):
    labels = []
    f = open(filename,'r')
    for line in f:
        labels.append(int(float(line)))
    
    f.close()    
    return labels


def label_index_from_file(filename):
    print('label_index_from_file')
    label_index = []
    f = open(filename,'rb')
    npt = struct.unpack('i',f.read(4))[0]
    print('npt',npt)
    for i in range(npt):
        label_index.append(struct.unpack('i',f.read(4))[0])
    
    f.close()    
    return label_index


from OCC.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCC.TCollection import TCollection_HAsciiString
from OCC.STEPConstruct import stepconstruct_FindEntity
from OCC.StepRepr import Handle_StepRepr_RepresentationItem
from OCC.TopLoc import TopLoc_Location

from occ_utils import set_face
                             
'''
input
    filename
    shape
    id_map： {TopoDS_Face: int}
output
'''
def shape_with_fid_to_step(filename, shape, id_map):
    print('shape_with_fid_to_step')
#    fset = set_face(shape)
    writer = STEPControl_Writer()    
    writer.Transfer(shape, STEPControl_AsIs)       
    
    finderp = writer.WS().GetObject().TransferWriter().GetObject().FinderProcess()
    
    fset = set_face(shape)

    loc = TopLoc_Location()
    for f in fset:
        item = stepconstruct_FindEntity(finderp, f, loc)
        if item.IsNull():
            print(f)            
            continue
        item.GetObject().SetName(TCollection_HAsciiString(str(id_map[f])).GetHandle())
        
    writer.Write(filename)

      
    
# to do
'''
input
output
    shape:      TopoDS_Shape
    id_map:  {TopoDS_Face: int}
'''
def shape_with_fid_from_step(filename):
    print('shape_with_fid_from_step')
    reader = STEPControl_Reader()
    reader.ReadFile(filename)
    reader.TransferRoots()    
    shape = reader.OneShape()
    
    tr = reader.WS().GetObject().TransferReader().GetObject()
    
    id_map = {}
    fset = set_face(shape)    
    # read the face names
    for f in fset:
        item = tr.EntityFromShapeResult(f, 1)
        if item.IsNull():
            print(f)
            continue
        item = Handle_StepRepr_RepresentationItem.DownCast(item).GetObject()
        name = item.Name().GetObject().ToCString()
        if name:
            nameid = int(name)
            id_map[f] = nameid

    return shape, id_map
    
if __name__ == '__main__':
    pts, normals, segs = point_cloud_from_file('D:/Weijuan/dataset/ModelNet40/ModelNet40/airplane/test/airplane_0627.points', False) 
    print(len(pts))           