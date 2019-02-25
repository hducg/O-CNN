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
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
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

    
from OCC.AIS import AIS_ColoredShape
from OCC.Display.SimpleGui import init_display
    
if __name__ == '__main__':
    # test write
#    shape = BRepPrimAPI_MakeBox(10, 20, 30).Solid()
#    filename = 'test_box.step'
#    fset = set_face(shape)
#    id_map = {}
#    fid = 0
#    for f in fset:
#        id_map[f] = fid
#        fid += 1
#    failed = shape_with_fid_to_step(filename, shape, id_map)
#    print(failed)
    
    # test read
    filename = 'boss-1(1[triangle2])2(2[sweep])2(2[sweep])3(3[sweep]).step'
    shape, id_map = shape_with_fid_from_step(filename)
    sorted_id = [v for k, v in sorted(id_map.items(), key = lambda kv: kv[1])]
    fset = set_face(shape)
    print('fset length', len(fset))
    fset1 = {f for f in id_map}
    print('fset1 length', len(fset1))
        
    occ_display, start_occ_display, add_menu, add_function_to_menu = init_display()    
    occ_display.EraseAll()
    
    ais = AIS_ColoredShape(shape)  
    occ_display.Context.Display(ais.GetHandle())
    occ_display.View_Iso()
    occ_display.FitAll()
    start_occ_display()    