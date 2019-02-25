# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:57:43 2018

@author: 2624224
"""

from math import pi
import random

from OCC.BRepBuilderAPI import (BRepBuilderAPI_Transform, BRepBuilderAPI_MakeWire,
                                BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace)
from OCC.BRepFeat import BRepFeat_MakePrism
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Ax1, gp_Trsf, gp_Vec, gp_OZ, gp_Circ
from OCC.TopAbs import TopAbs_REVERSED 
from OCC.TopoDS import topods
from OCC.BRepTools import breptools_UVBounds
from OCC.BRep import BRep_Tool_Surface
from OCC.GeomLProp import GeomLProp_SLProps
from OCC.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.TopTools import TopTools_ListIteratorOfListOfShape

from occ_utils import set_face

drain_R = 10.0
drain_r = 0.5
drain_t = 0.5
drain_rcs = gp_Ax2(gp_Pnt(0,0,0),gp_Dir(0,0,1))


'''
    standard circle on XY plane, centered at origin, with radius 1

output
    w:     TopoDS_Wire
'''
def wire_circle():
    
    c = gp_Circ(drain_rcs,1.0)   
    e = BRepBuilderAPI_MakeEdge(c, 0., 2*pi).Edge()
    w = BRepBuilderAPI_MakeWire(e).Wire()     
    
    return w


'''
    equal sided triangle, centered at origin
output
    w:  TopoDS_Wire
'''
def wire_triangle3():
    p1 = gp_Pnt(-1,0,0)
    p2 = gp_Pnt(-1,0,0)
    p2.Rotate(gp_OZ(),2*pi/3)
    p3 = gp_Pnt(-1,0,0)
    p3.Rotate(gp_OZ(),4*pi/3)
    
    e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
    e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
    e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p1).Value()).Edge()
    
    w = BRepBuilderAPI_MakeWire(e1,e2,e3).Wire()

    return w


'''
    isosceles triangle
output
    w:  TopoDS_Wire
'''
def wire_triangle2():
    ang = random.gauss(2*pi/3, pi/6)
    amin = pi / 3
    amax = 5 * pi / 6 
    if (ang > amax):
        ang = amax
    if (ang < amin):
        ang = amin
    p1 = gp_Pnt(-1,0,0)
    p2 = gp_Pnt(-1,0,0)
    p2.Rotate(gp_OZ(),ang)
    p3 = gp_Pnt(-1,0,0)
    p3.Rotate(gp_OZ(),-ang)
    
    e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
    e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
    e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p1).Value()).Edge()
    
    w = BRepBuilderAPI_MakeWire(e1,e2,e3).Wire()

    return w    


'''
output
    w:  TopoDS_Wire
'''
def wire_rectangle():
    p1 = gp_Pnt(0,1,0)
    p2 = gp_Pnt(-1,0,0)
    p3 = gp_Pnt(0,-1,0)
    p4 = gp_Pnt(1,0,0)
    
    e1 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p1, p2).Value()).Edge()
    e2 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p2, p3).Value()).Edge()
    e3 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p3, p4).Value()).Edge()
    e4 = BRepBuilderAPI_MakeEdge(GC_MakeSegment(p4, p1).Value()).Edge()   
    
    w = BRepBuilderAPI_MakeWire(e1,e2,e3,e4).Wire()

    return w


'''
input
    c1:     gp_Pnt
    c2:     gp_Pnt
output
    w:      TopoDS_Wire
'''
def wire_sweep_circle(c1, c2):
    P = drain_rcs.Location()
    V = drain_rcs.Direction()
    
    R = P.Distance(c1)
    
    p1 = gp_Pnt(c1.XYZ())
    p2 = gp_Pnt(c1.XYZ())
    p3 = gp_Pnt(c2.XYZ())
    p4 = gp_Pnt(c2.XYZ())

    v1 = gp_Vec(c1,P)
    v1.Normalize()
    v2 = gp_Vec(c2, P)
    v2.Normalize()
    
    p1.Translate(v1*drain_r)
    p2.Translate(-v1*drain_r)        
    p3.Translate(v2*drain_r)
    p4.Translate(-v2*drain_r)
    
    s1 = gp_Circ(gp_Ax2(c1,V),drain_r)
    e1 = BRepBuilderAPI_MakeEdge(GC_MakeArcOfCircle(s1, p1, p2, True).Value()).Edge()
    
    s2 = gp_Circ(gp_Ax2(P,V), R + drain_r)
    e2 = BRepBuilderAPI_MakeEdge(GC_MakeArcOfCircle(s2, p2, p4, False).Value()).Edge()
    
    s3 = gp_Circ(gp_Ax2(c2,V),drain_r)
    e3 = BRepBuilderAPI_MakeEdge(GC_MakeArcOfCircle(s3, p4, p3, True).Value()).Edge()
    
    s4 = gp_Circ(gp_Ax2(P,V), R - drain_r)
    e4 = BRepBuilderAPI_MakeEdge(GC_MakeArcOfCircle(s4, p1, p3, False).Value()).Edge()
    
    w = BRepBuilderAPI_MakeWire(e1,e2,e3,e4).Wire()
    
    return w

    
# list of wire generation function 
flist = [wire_circle, wire_rectangle, wire_triangle2, wire_sweep_circle]
sketch_type = ['circle', 'rectangle', 'triangle2', 'sweep']
feat_type = ['hole', 'blind', 'boss']
label_index = {'ohter':0, 'base':1, 'hole_triangle2':2, 'hole_rectangle':3, 'hole_circle':4, 'hole_sweep':5,
               'blind_triangle2':6, 'blind_rectangle':7, 'blind_circle':8,'blind_sweep':9, 
               'boss_triangle2':10, 'boss_rectangle':11,'boss_circle':12,'boss_sweep':13}

               
'''
    find the length of the natural sequence from pos, pos is an element of pos_list
input
    pos:        int
    pos_list:   [int]
output
    j - i:      int
'''
def len_seq_natural(pos, pos_list):
    i = pos_list.index(pos)
    j = i + 1
    while j < len(pos_list):
        if pos_list[j] != pos_list[j - 1] + 1:
            break
        j += 1    
    return j - i


'''
input
   nc:              int, number of cells to be combined
   ang:             float, angle between adjaent cells
   offset:          float, offset angle of start position
   ri:              float, radius of this ring
output
    wlist:          {TopoDS_Wire: string}
    combo_name:     ''
'''
def list_wire_combo(nc, ang, offset, ri):
    combo_name = ''    
#    fname = ['wire_circle', 'wire_rectangle', 'wire_triangle3', 'wire_triangle2', 'wire_sweep_circle']            
    pos_list = list(range(nc))
    wlist = {}
    pos_len_name = {}
    while len(pos_list)>0:
#       1 choose a random location
        pos = random.choice(pos_list)

#       2 choose a random length
        l = len_seq_natural(pos, pos_list)
        l = random.randrange(1, l + 1)
        
#       3 choose a random shape
        func = random.choice(flist)
#        print(pos_list, pos, l, fname[flist.index(func)])
        ts = gp_Trsf()
        ts.SetScale(drain_rcs.Location(), drain_r)
        tt = gp_Trsf()
        tv = gp_Vec(drain_rcs.XDirection()) * ri
        tt.SetTranslation(tv)
        tr = gp_Trsf()
        tr.SetRotation(gp_Ax1(drain_rcs.Location(),drain_rcs.Direction()), offset + pos * ang)
        if(func == wire_sweep_circle and l > 1):
            c1 = drain_rcs.Location()
            c2 = drain_rcs.Location()
            c1.Translate(tv)
            c1.Rotate(gp_Ax1(drain_rcs.Location(),drain_rcs.Direction()), offset + pos * ang)
            c2.Translate(tv)
            c2.Rotate(gp_Ax1(drain_rcs.Location(),drain_rcs.Direction()), offset + (pos + l -1) * ang)
            w = wire_sweep_circle(c1, c2)            
        elif(func != wire_sweep_circle and l == 1):
            w = func()
            aBRespTrsf = BRepBuilderAPI_Transform(w,ts)
            w = topods.Wire(aBRespTrsf.Shape())
            aBRespTrsf = BRepBuilderAPI_Transform(w,tt)
            w = topods.Wire(aBRespTrsf.Shape())
            aBRespTrsf = BRepBuilderAPI_Transform(w,tr)
            w = topods.Wire(aBRespTrsf.Shape())
        else:
            continue
        
        wname = sketch_type[flist.index(func)]
        pos_len_name[pos] = (l, wname)                                        
        wlist[w] = wname
        for pos in range(pos, pos + l):
            pos_list.remove(pos)
    
    pos_len_name = sorted(pos_len_name.items(), key=lambda t : t[0])    
    for pos in pos_len_name:
        combo_name += str(pos[1][0]) + '[' + pos[1][1] + ']'
    return wlist, combo_name


'''
output
    wires:      {TopoDS_Wire:string}
    wire_name:  ''
'''
def list_wire_random():
    wire_name = ''    
    #    number of rings
    nr = int((drain_R/4/drain_r-0.5))
    wires = {}
    
    for i in range(nr):
#        radius of ith ring
        ri = 3*drain_r+i*4*drain_r
#        number of cells per ring
        np = int(1.5*pi+2*pi*i)
#        print('np:',np)
        
#        randomly choose the number of cells to combine
        combo_list = range(1, np // 3 + 1)
        combo = random.choice(combo_list)
#        angle between two adjacent cells
        ang = 2 * pi / np        
#        randomly offset the start cell
        offset = random.gauss(ang / 2, ang / 2)
        if (offset < 0.):
            offset = 0.
        if(offset > ang):
            offset = ang
        wlist, combo_name = list_wire_combo(combo, ang, offset, ri)        
        wires.update(wlist)
        wire_name += str(combo) + '(' + combo_name + ')'
        np = np // combo       
#        print('combo',combo,'repeat',np)        

        ang = 2*pi/np
        for j in range(1, np):            
            aTrsf = gp_Trsf()
            aTrsf.SetRotation(gp_Ax1(drain_rcs.Location(), drain_rcs.Direction()), ang * j)
            for w in wlist:
                wname = wlist[w]
                aBRespTrsf = BRepBuilderAPI_Transform(w, aTrsf)
                w = topods.Wire(aBRespTrsf.Shape())
                wires[w] = wname
                
    return wires, wire_name


'''
input
    face: TopoDS_Face
output
    gp_Dir
'''
def normal_face(face):
    u, u_max, v, v_max = breptools_UVBounds(face)
    surf = BRep_Tool_Surface(face)    
    D = GeomLProp_SLProps(surf,u,v,1,0.01).Normal()  
    if face.Orientation() == TopAbs_REVERSED:
        D.Reverse()
    
    return D    


'''
input
    s: TopoDS_Shape
output
    f: TopoDS_Face
'''
def face_bottom(s):
    flist = set_face(s)
    for f in flist:
        d = normal_face(f)
        if (d.IsEqual(drain_rcs.Direction(),0.01)):
            break
        
    return f


'''
input
    base: TopoDS_Shape
    feature_maker: BRepFeat_MakePrism
output
    fmap: {TopoDS_Face:TopoDS_Face}
'''
def map_face_before_and_after_feat(base, feature_maker):       
    fmap = {}
    base_faces = set_face(base)
    
    for f in base_faces:
        if feature_maker.IsDeleted(f):
            continue
        
        fmap[f] = []
        modified = feature_maker.Modified(f)
        if modified.IsEmpty():
            fmap[f].append(f)
            continue
        
        occ_it = TopTools_ListIteratorOfListOfShape(modified)
        while occ_it.More():
            fmap[f].append(occ_it.Value())
            occ_it.Next()

    return fmap                  


'''
input
    shape: TopoDS_Shape
    name: string
output
    name_map: {TopoDS_Face: string}
'''
def map_from_name(shape, name):
    name_map = {}
    faces = set_face(shape)
    
    for f in faces:
        name_map[f] = name
    
    return name_map


'''
input
    fmap: {TopoDS_Face: TopoDS_Face}, 
    old_map: {TopoDS_Face: int}
    new_shape: TopoDS_Shape
    new_name: string
output
    new_map: {TopoDS_Face: int}
'''
def map_from_shape_and_name(fmap, old_map, new_shape, new_name):            
    new_map = {}
    new_faces = set_face(new_shape)
    for oldf in fmap:
        old_name = old_map[oldf]
        for samef in fmap[oldf]:
            new_map[samef] = old_name
            new_faces.remove(samef)
    
    for f in new_faces:
        new_map[f] = new_name

    return new_map 

        
'''
    one face and one hole feature for each wire
input
    base:       TopoDS_Shape
    wlist:      {TopoDS_Wire:string}
output
    base:       TopoDS_Shape
    name_map:   {TopoDS_Face:int}
    ftype:      ''
'''
def shape_multiple_hole_feats(base, wlist):    
    F = face_bottom(base)
    random.shuffle(feat_type)
    ftype = random.choice(feat_type)    
    if ftype == 'hole':
        direction = drain_rcs.Direction()
        fuse = False
        length = drain_t
    elif ftype == 'blind':
        direction = drain_rcs.Direction()
        fuse = False
        length = drain_t / 3
    else:
        direction = -drain_rcs.Direction()
        fuse = True
        length = drain_t / 2
    
    base_map = map_from_name(base, label_index['base'])
    for w in wlist:            
        FP = BRepBuilderAPI_MakeFace(w).Face()           
        feature_maker = BRepFeat_MakePrism() 
        feature_maker.Init(base, FP, F, direction, fuse, False)
        feature_maker.Build()
        
        feature_maker.Perform(length)        
        shape = feature_maker.Shape()
                        
        fmap = map_face_before_and_after_feat(base,feature_maker)        
        name_map = map_from_shape_and_name(fmap, base_map, shape, label_index[ftype + '_' + wlist[w]])
        
        base = shape
        base_map = name_map
              
    return base, base_map, ftype


'''
output
    s: TopoDS_Shape
'''
def shape_base_drain():
    w = wire_circle()
    
    ts = gp_Trsf()
    ts.SetScale(drain_rcs.Location(), drain_R)
    aBRespTrsf = BRepBuilderAPI_Transform(w,ts)
    w = topods.Wire(aBRespTrsf.Shape()) 
    
    F = BRepBuilderAPI_MakeFace(w).Face()    
    s = BRepPrimAPI_MakePrism(F, gp_Vec(0,0,drain_t)).Shape()
    
    return s         


'''
output
    shape:          TopoDS_Shape
    face_map:       {TopoDS_Face: int}
    id_map:         {TopoDS_Face: int}
    shape_name:     ''
'''                
def shape_drain():    
#    step1, create the base
    base = shape_base_drain()    
    
#    step2, create wires for holes
    wlist, wire_name = list_wire_random()       
    
#    step3, add hole feature from wire
    shape, name_map, feat_name = shape_multiple_hole_feats(base, wlist)
    
    shape_name = feat_name + '-' + wire_name
    
    fid= 0
    fset = set_face(shape)
    id_map = {}
    for f in fset:
        id_map[f] = fid
        fid += 1
   
    return shape, name_map, id_map, shape_name

    
from data_import_export import shape_with_fid_to_step, shape_with_fid_from_step        
import pickle

if __name__ == '__main__':
    print('model_factory.py')
    from OCC.AIS import AIS_ColoredShape
    from OCC.Display.SimpleGui import init_display
    from OCC.Display.OCCViewer import rgb_color
    
    occ_display, start_occ_display, add_menu, add_function_to_menu = init_display()    
    occ_display.EraseAll()
    
    colors = [rgb_color(0,0,0), rgb_color(0.75,0.75,0.75), 
          rgb_color(1,0,0), rgb_color(1,0.5,0), rgb_color(0,1,1), rgb_color(1,0,1), 
          rgb_color(1,0.8,0.8), rgb_color(1,1,0.8), rgb_color(0.8,1,1), rgb_color(1,0.8,1), 
          rgb_color(0.4,0,0), rgb_color(0.4,0.4,0), rgb_color(0,0.4,0.4), rgb_color(0.4,0,0.4)] 

#    shape, fmap, id_map, shape_name = shape_drain()
#    print(shape_name)
#    face_truth = [fmap[f] for f, fid in sorted(id_map.items(), key = lambda kv: kv[1])]
#    with open(shape_name + '.face_truth', 'wb') as f:
#        pickle.dump(face_truth, f)

    shape_name = 'hole-1(1[triangle2])2(2[sweep])1(1[rectangle])7(1[rectangle]1[rectangle]1[circle]1[rectangle]1[circle]1[rectangle]1[rectangle])'
    shape, id_map = shape_with_fid_from_step(shape_name + '.step')
    with open(shape_name + '.face_truth', 'rb') as f:
        face_truth = pickle.load(f)        
    
    fmap = {f: face_truth[id_map[f]] for f in id_map}    
    ais = AIS_ColoredShape(shape)    
    for f in fmap:        
        ais.SetCustomColor(f, colors[fmap[f]])

#    filename = shape_name + '.step'    
#    failed = shape_with_fid_to_step(filename, shape, id_map)   
        
#    for f in failed:
#        ais.SetCustomColor(f, rgb_color(0,0,0))
        
    occ_display.Context.Display(ais.GetHandle())
    occ_display.View_Iso()
    occ_display.FitAll()
            
    start_occ_display()
           