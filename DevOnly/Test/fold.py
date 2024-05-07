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
  
def angle_bisect(e1_index, e2_index):
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

def door_fold(e1_index, e2_index):
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
  
  e1_middle = (e1.verts[0].co + e1.verts[1].co) / 2
  e2_middle = (e2.verts[0].co + e2.verts[1].co) / 2
  
  bisect_point = (e1_middle + e2_middle) / 2
  bisect_plane_normal = (e2_middle - e1_middle).normalized()

  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=bisect_point, plane_no=bisect_plane_normal)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  new_edge = bm.edges[-1]
  axis = new_edge.verts[0].co - new_edge.verts[1].co
  
  Ti = mathutils.Matrix.Translation(new_edge.verts[0].co * -1)
  R = mathutils.Matrix.Rotation(math.pi * 0.995, 4, axis)
  T = mathutils.Matrix.Translation(new_edge.verts[0].co)
  
  TRTi = T @ R @ Ti

  target_indices = set()
  for vert in e1.verts:
      for link_edge in vert.link_edges:
          for target_vert in link_edge.verts:
              target_indices.add(target_vert.index)

  for index in target_indices:
      target_vert = bm.verts[index]
      target_vert.co = TRTi @ target_vert.co
  
  bm.free()

def fish_fold():
  return 1

def double_boat_fold():
  return 1

def pocket_fold():
  return 1

door_fold(0,2)
door_fold(1,5)