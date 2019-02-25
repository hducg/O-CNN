# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 15:37:43 2018

@author: 2624224
"""

##Copyright 2010-2017 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import numpy as np
import math
from multiprocessing import Pool

##########################
# OCC library
##########################
from OCC.BRepAdaptor import BRepAdaptor_Surface
from OCC.BRepMesh import BRepMesh_IncrementalMesh
from OCC.BRep import BRep_Tool, BRep_Tool_Surface
from OCC.TopLoc import TopLoc_Location
from OCC.GeomLProp import GeomLProp_SLProps
from OCC.TopAbs import TopAbs_REVERSED

#==============================================================================
# local library
#==============================================================================
from occ_utils import set_face, get_boundingbox

#logging.basicConfig(level=logging.INFO)
#
#logger = logging.getLogger(__name__)


    
'''
input
    shape:          TopoDS_Shape
output
    pts:            [[float,float,float]]
    uvs:            [[float,float]]
    triangles:   [[int,int,int]]
    triangle_faces: [TopoDS_Face]    
'''    
def triangulation_from_shape(shape):
    linear_deflection = 0.9
    angular_deflection = 0.5
    mesh = BRepMesh_IncrementalMesh(shape, linear_deflection, False, angular_deflection, True)
    mesh.Perform()
    assert mesh.IsDone()
    
    pts = []
    uvs = []
    triangles = []
    triangle_faces = []
    faces = set_face(shape)
    offset = 0
    for f in faces:
        aLoc = TopLoc_Location()
        aTriangulation = BRep_Tool().Triangulation(f, aLoc).GetObject()
        aTrsf = aLoc.Transformation()
        aOrient = f.Orientation()

        aNodes = aTriangulation.Nodes()
        aUVNodes = aTriangulation.UVNodes()
        aTriangles = aTriangulation.Triangles()
        
        for i in range(1, aTriangulation.NbNodes() + 1):
            pt = aNodes.Value(i)
            pt.Transform(aTrsf)
            pts.append([pt.X(),pt.Y(),pt.Z()])
            uv = aUVNodes.Value(i)
            uvs.append([uv.X(),uv.Y()])
        
        for i in range(1, aTriangulation.NbTriangles() + 1):
            n1, n2, n3 = aTriangles.Value(i).Get()
            n1 -= 1
            n2 -= 1
            n3 -= 1
            if aOrient == TopAbs_REVERSED:
                tmp = n1
                n1 = n2
                n2 = tmp
            n1 += offset
            n2 += offset
            n3 += offset
            triangles.append([n1, n2, n3])
            triangle_faces.append(f)
        offset += aTriangulation.NbNodes()

    return pts, uvs, triangles, triangle_faces

    
'''
input
    uv1:    [float,float]
    uv2:    [float,float]
    uv3:    [float,float]
    N1:     int
    N2:     int
output
    uvs:    [[float,float]]
'''    
def uvs_from_interpolation(uv1, uv2, uv3, N1, N2):
    uvs = []
    for i in range(N1 + 1):#[0, N1]
        t1 = i / N1#[0, 1]
        uv12 = np.multiply(uv2, t1) + np.multiply(uv1, 1 - t1)#[uv1, uv2]
        uv13 = np.multiply(uv3, t1) + np.multiply(uv1, 1 - t1)#[uv1, uv3]
        N12 = int(N2 * t1) + 1 #[1, N2 + 1]
        for j in range(N12):#[0, 1] [0, N2]
            t2 = j / N12 #[0, 1]
            uv = np.multiply(uv12, t2) + np.multiply(uv13, 1 - t2)#uv12 * t2 + uv13 * (1 - t2)
            uvs.append(uv)
            
    return uvs 
    
    
'''
input
    t:          ([[float,float,float],[float,float,float],[float,float,float]],
                  [[float,float],[float,float],[float,float]],
                  TopoDS_Face,
                  float)
output
    samples:        [[float,float,float]]
    normals:    [[float,float,float]]
    f:          TopoDS_Face
'''    
def points_sample_from_triangle(t):
    samples = []
    normals = []

    p1 = np.array(t[0][0])
    p2 = np.array(t[0][1])
    p3 = np.array(t[0][2])
    resolution = t[3]
    N1 = int(np.sqrt(np.sum(np.square(p1 - p2))) / resolution) 
    N2 = int(np.sqrt(np.sum(np.square(p1 - p3))) / resolution)
    
    uv1 = t[1][0]
    uv2 = t[1][1]
    uv3 = t[1][2]
    
    uvs = uvs_from_interpolation(uv1,uv2,uv3,N1,N2)
    f = t[2]
    surf = BRep_Tool_Surface(f)
    for uv in uvs:
        pt = BRepAdaptor_Surface(f).Value(uv[0],uv[1])                
        samples.append([pt.X(),pt.Y(),pt.Z()])
        #   the normal
        D = GeomLProp_SLProps(surf,uv[0],uv[1],1,0.01).Normal()  
        if f.Orientation() == TopAbs_REVERSED:
            D.Reverse()
        normals.append([D.X(),D.Y(),D.Z()])
         
    return (samples, normals, f)


'''
input
    shape: TopoDS_Shape
    resolution: float        
output
    traingles: [([],[],TopoDS_Face,float)]
'''
def triangles_from_shape(shape, resolution):
    tri_pts, tri_uvs, tri_facets, tri_faces = triangulation_from_shape(shape)
    triangles = []
    for i in range(len(tri_facets)):
        t_idx = tri_facets[i]
        pts = []
        uv= []
        for idx in t_idx:
            pts.append(tri_pts[idx])
            uv.append(tri_uvs[idx])
        f= tri_faces[i]   
        triangles.append((pts,uv,f,resolution)) 

    return triangles

        
'''
input
    shape:      TopoDS_Shape
    name_map:   {TopoDS_Face:{'label':int, 'id':int}}
    resolution: float
output
    cloud_pts:      [[float,float,float]]
    cloud_normals:  [[float,float,float]]
    cloud_segs:     [int]
    face_ids:       [int]
'''    
def point_cloud_from_labeled_shape(shape, label_map, id_map, resolution=0.1):    
    cloud_pts = []
    cloud_normals = []
    cloud_segs = []
    face_ids = []
    triangles = triangles_from_shape(shape, resolution)   
    for t in triangles:
        r = points_sample_from_triangle(t)
        cloud_pts += r[0]
        cloud_normals += r[1]        
        cloud_segs += [label_map[r[2]]] * len(r[0])
        face_ids += [id_map[r[2]]] * len(r[0])            
    return cloud_pts, cloud_normals, cloud_segs, face_ids


'''
input
    shape:          TopoDS_Shape
output
    resolution:     float
'''    
def resolution_from_shape(shape):
    xmin, ymin, zmin, xmax, ymax, zmax, xlen, ylen, zlen = get_boundingbox(shape, use_mesh = False)
    area = (xlen * ylen + xlen * zlen + ylen * zlen) * 2
    resolution = math.sqrt(area / 1.0e5)
    
    return resolution        

        
if __name__ == '__main__':
    print('test point_cloud.py')
    import random
    from model_factory import shape_drain
    from OCC.Display.SimpleGui import init_display
    from data_render import display_point_cloud

    occ_display, start_occ_display, add_menu, add_function_to_menu = init_display()    
    occ_display.EraseAll()
    
    random.seed()

    shape, name_map, shape_name = shape_drain()
    pts, normals, segs = point_cloud_from_labeled_shape(shape, name_map)
    
    ais_context = occ_display.GetContext().GetObject()
    display_point_cloud(pts,segs,ais_context)
        
    occ_display.View_Iso()
    occ_display.FitAll()
    start_occ_display()