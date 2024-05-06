import bpy
import bmesh
import mathutils
import math

from mathutils.geometry import *

def v2v_fold():
  return 1

def e2e_fold():
  return 1

def perpendicular_bisect(v1_index, v2_index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.context.tool_settings.mesh_select_mode = (False, False, True)
  bpy.ops.mesh.select_all(action='DESELECT')
  
  bm = bmesh.from_edit_mesh(obj.data)

  bm.select_flush(False)
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  v1 = bm.verts[v1_index]
  v2 = bm.verts[v2_index]
    
  vec1 = v1.co
  vec2 = v2.co
  
  bisect_point = (vec1 + vec2) / 2
  v1v2 = vec2-vec1
  
  for face in v1.link_faces:
      face.select_set(True)
        
  bpy.ops.mesh.bisect(plane_co=bisect_point, plane_no=v1v2)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  bm.free()

def triangle_fold(v1_index, v2_index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.context.tool_settings.mesh_select_mode = (False, False, True)
  bpy.ops.mesh.select_all(action='DESELECT')
  
  bm = bmesh.from_edit_mesh(obj.data)

  bm.select_flush(False)
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  v1 = bm.verts[v1_index]
  v2 = bm.verts[v2_index]
    
  vec1 = v1.co
  vec2 = v2.co
  
  bisect_point = (vec1 + vec2) / 2
  v1v2 = vec2-vec1
  
  for face in v1.link_faces:
      face.select_set(True)
        
  bpy.ops.mesh.bisect(plane_co=bisect_point, plane_no=v1v2)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  new_edge = bm.edges[-1]
  axis = new_edge.verts[0].co - new_edge.verts[1].co
  
  R = mathutils.Matrix.Rotation(math.pi * 0.995, 3, axis)

  v1.co = R @ v1.co
  
  bm.free()
  

def icecream_fold(e1_index, e2_index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.context.tool_settings.mesh_select_mode = (False, False, True)
  bpy.ops.mesh.select_all(action='DESELECT')
  
  bm = bmesh.from_edit_mesh(obj.data)

  bm.select_flush(False)
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  e1 = bm.edges[e1_index]
  e2 = bm.edges[e2_index]
  
  e1_unit = (e1.verts[1].co - e1.verts[0].co).normalized()
  e2_unit = (e2.verts[1].co - e2.verts[0].co).normalized()
  
  angle_bisector = (e1_unit + e2_unit)
  face_normal = e1_unit.cross(e2_unit)
  bisect_plane_normal = angle_bisector.cross(face_normal).normalized()
  
  intersection_points = intersect_line_line(e1.verts[0].co, e1.verts[1].co, e2.verts[0].co, e2.verts[1].co)
  intersection_point = intersection_points[0]
  
  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=intersection_point, plane_no=bisect_plane_normal)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  new_edge = bm.edges[-1]
  axis = new_edge.verts[0].co - new_edge.verts[1].co
  
  Ti = mathutils.Matrix.Translation(intersection_point * -1)
  R = mathutils.Matrix.Rotation(math.pi * 0.995, 4, axis)
  T = mathutils.Matrix.Translation(intersection_point)
  
  TRTi = T @ R @ Ti

  for vert in e1.verts:
      vert.co = TRTi @ vert.co
  
  bm.free()

def door_fold(edge1, edge2):
  return 1

def fish_fold():
  return 1

def double_boat_fold():
  return 1

def pocket_fold():
  return 1

def test_triangle_fold(v1, v2):
  vec1 = v1.co
  vec2 = v2.co
  
  v1v2 = vec2-vec1
  n = v1.normal
  
  bisect_vec = n.cross(v1v2)
  bisect_point = (vec1 + vec2) / 2
  
  adj_edges = [e for e in v1.link_edges]
  intersection_points = [] 
  
  for edge in adj_edges:
      edge_start, edge_end = [v.co for v in edge.verts]
      intersection_point = intersect_line_line(bisect_point, bisect_point + bisect_vec, edge_start, edge_end)
      intersection_points.append(intersection_point[0])

  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.context.tool_settings.mesh_select_mode = (True, False, False)
  bpy.ops.mesh.select_all(action='DESELECT')
  
  # 메시 데이터를 수정하기 위해 bmesh 불러오기
  bm = bmesh.from_edit_mesh(obj.data)
  
  # 모든 선택 해제
  bm.select_flush(False)
  bm.verts.ensure_lookup_table()

  # print(intersection_points[0])
  # bm.verts.new(intersection_points[0])
  # bm.verts.new(intersection_points[1])
  
  bpy.ops.mesh.bisect(plane_co=(0.0, 0.0, 0.0), plane_no=v1v2, use_fill=False, clear_inner=False, clear_outer=False, threshold=0.0001, xstart=10, xend=-10, ystart=10, yend=-10)
  
  bm.verts.ensure_lookup_table()
  bm.free()

perpendicular_bisect(1,2)
icecream_fold(2,4)