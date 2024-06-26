import bpy
import bmesh
import mathutils
import math

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
  
  for face in bm.faces:
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
  
  intersection_points = mathutils.geometry.intersect_line_line(e1.verts[0].co, e1.verts[1].co, e2.verts[0].co, e2.verts[1].co)
  intersection_point = intersection_points[0]
  
  e1_unit = ((e1.verts[0].co - intersection_point) + (e1.verts[1].co - intersection_point)).normalized()
  e2_unit = ((e2.verts[0].co - intersection_point) + (e2.verts[1].co - intersection_point)).normalized()
  
  angle_bisector = (e1_unit + e2_unit)
  face_normal = e1_unit.cross(e2_unit)
  bisect_plane_normal = angle_bisector.cross(face_normal).normalized()
  
  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=intersection_point, plane_no=bisect_plane_normal)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  bm.free()


def parallel_bisect(e1_index, e2_index):
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
  
  A,B = [v.co for v in e1.verts]
  C,D = [v.co for v in e2.verts]

  face_normal = (C-A).cross(D-A).normalized()
  e1_unit = (B-A).normalized()
  
  bisect_point = (A+B+C+D) / 4
  bisect_plane_normal = face_normal.cross(e1_unit).normalized()

  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=bisect_point, plane_no=bisect_plane_normal)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  bm.free()
  
  
def bisect(plane_co, plane_no):
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
  
  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=plane_co, plane_no=plane_no)
  
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
  
  R = mathutils.Matrix.Rotation(math.pi, 3, axis)

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
  
  intersection_points = mathutils.geometry.intersect_line_line(e1.verts[0].co, e1.verts[1].co, e2.verts[0].co, e2.verts[1].co)
  intersection_point = intersection_points[0]
  
  e1_unit = ((e1.verts[0].co - intersection_point) + (e1.verts[1].co - intersection_point)).normalized()
  e2_unit = ((e2.verts[0].co - intersection_point) + (e2.verts[1].co - intersection_point)).normalized()
  
  angle_bisector = (e1_unit + e2_unit)
  face_normal = e1_unit.cross(e2_unit)
  bisect_plane_normal = angle_bisector.cross(face_normal).normalized()
  
  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=intersection_point, plane_no=bisect_plane_normal)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  new_edge = bm.edges[-1]
  axis = new_edge.verts[0].co - new_edge.verts[1].co
  
  Ti = mathutils.Matrix.Translation(intersection_point * -1)
  R = mathutils.Matrix.Rotation(math.pi, 4, axis)
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
  
  A,B = [v.co for v in e1.verts]
  C,D = [v.co for v in e2.verts]

  face_normal = (C-A).cross(D-A).normalized()
  e1_unit = (B-A).normalized()
  
  bisect_point = (A+B+C+D) / 4
  bisect_plane_normal = face_normal.cross(e1_unit).normalized()

  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=bisect_point, plane_no=bisect_plane_normal)
  
  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  new_edge = bm.edges[-1]
  axis = new_edge.verts[0].co - new_edge.verts[1].co
  
  Ti = mathutils.Matrix.Translation(new_edge.verts[0].co * -1)
  R = mathutils.Matrix.Rotation(math.pi, 4, axis)
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
  

def reverse_fold(v_index, e_indices):
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
  
  e1 = bm.edges[e_indices[0]]
  e2 = bm.edges[e_indices[1]]
  
  e1_unit = (e1.verts[1].co - e1.verts[0].co).normalized()
  e2_unit = (e2.verts[1].co - e2.verts[0].co).normalized()
  
  e1_middle = (e1.verts[0].co + e1.verts[1].co) / 2
  e2_middle = (e2.verts[0].co + e2.verts[1].co) / 2
  
  axis = (e1_unit + e2_unit).normalized()
  axis_point = (e1_middle + e2_middle) / 2
  
  Ti = mathutils.Matrix.Translation(axis_point * -1)
  R = mathutils.Matrix.Rotation(math.pi, 4, axis)
  T = mathutils.Matrix.Translation(axis_point)
  
  TRTi = T @ R @ Ti

  target_vertex = bm.verts[v_index]
  target_vertex.co = TRTi @ target_vertex.co
  
  bm.free()


def v1v2_axis_fold(v_index, v1_index, v2_index, angle=math.pi):
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
  
  v = bm.verts[v_index]
  v1 = bm.verts[v1_index]
  v2 = bm.verts[v2_index]
  
  vv1 = v1.co - v.co
  vv2 = v2.co - v.co
  
  v1v2 = v2.co - v1.co
  
  bisect_point = (v1.co + v2.co) / 2
  bisect_plane_normal = vv1.cross(vv2).cross(v1v2).normalized()

  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=bisect_point, plane_no=bisect_plane_normal)

  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()
  
  new_edge = bm.edges[-1]
  axis = new_edge.verts[0].co - new_edge.verts[1].co
  
  Ti = mathutils.Matrix.Translation(new_edge.verts[0].co * -1)
  R = mathutils.Matrix.Rotation(angle, 4, axis)
  T = mathutils.Matrix.Translation(new_edge.verts[0].co)
  
  TRTi = T @ R @ Ti

  target_vertex = bm.verts[v_index]
  target_vertex.co = TRTi @ target_vertex.co
  
  bm.free()


def e_axis_fold(v_index, e_index, angle=math.pi):
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
  
  v = bm.verts[v_index]  
  e = bm.edges[e_index]

  v1 = e.verts[0]
  v2 = e.verts[1]
  
  vv1 = v1.co - v.co
  vv2 = v2.co - v.co
  
  v1v2 = v2.co - v1.co
  
  bisect_point = (v1.co + v2.co) / 2
  bisect_plane_normal = vv1.cross(vv2).cross(v1v2).normalized()

  for face in bm.faces:
    face.select_set(True)
  
  bpy.ops.mesh.bisect(plane_co=bisect_point, plane_no=bisect_plane_normal)

  bm.verts.ensure_lookup_table()
  bm.edges.ensure_lookup_table()
  bm.faces.ensure_lookup_table()

  axis = (e.verts[1].co - e.verts[0].co).normalized()
  axis_point = (e.verts[0].co + e.verts[1].co) / 2
  
  Ti = mathutils.Matrix.Translation(axis_point * -1)
  R = mathutils.Matrix.Rotation(angle, 4, axis)
  T = mathutils.Matrix.Translation(axis_point)
  
  TRTi = T @ R @ Ti

  v.co = TRTi @ v.co
  
  bm.free()
  
  
def rotate_v_around_e(v_index, e_index, angle=math.pi):
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
  
  v = bm.verts[v_index]
  e = bm.edges[e_index]

  axis = (e.verts[1].co - e.verts[0].co).normalized()
  axis_point = (e.verts[0].co + e.verts[1].co) / 2
  
  Ti = mathutils.Matrix.Translation(axis_point * -1)
  R = mathutils.Matrix.Rotation(angle, 4, axis)
  T = mathutils.Matrix.Translation(axis_point)
  
  TRTi = T @ R @ Ti

  v.co = TRTi @ v.co
  
  bm.free()