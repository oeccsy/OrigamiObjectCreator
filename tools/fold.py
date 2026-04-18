from mcp_instance import mcp
import bpy
import bmesh
import mathutils
import math

@mcp.tool()
def perpendicular_bisect(v1_index, v2_index) -> str:
  """
  두 꼭짓점(v1, v2)을 잇는 선분의 수직이등분면으로 메시 전체를 절단합니다.
  절단면은 v1과 v2의 중점을 지나고 v1→v2 방향을 법선으로 합니다.
  종이접기에서 점 v1을 점 v2에 맞추는 접기 선을 만들 때 사용합니다.
  Args:
      v1_index: 첫 번째 꼭짓점의 인덱스
      v2_index: 두 번째 꼭짓점의 인덱스
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"
  
@mcp.tool()
def angle_bisect(e1_index, e2_index) -> str:
  """
  두 엣지(e1, e2)의 교점에서 두 엣지가 이루는 각도를 이등분하는 평면으로 메시를 절단합니다.
  교점을 기준으로 각 이등분선 방향의 법선 평면을 계산하여 bisect 합니다.
  접기 선을 만들 때 사용합니다.
  Args:
      e1_index: 첫 번째 엣지의 인덱스
      e2_index: 두 번째 엣지의 인덱스
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"

@mcp.tool()
def parallel_bisect(e1_index, e2_index) -> str:
  """
  두 엣지(e1, e2)에 평행하고 두 엣지의 중간 지점을 지나는 평면으로 메시를 절단합니다.
  두 엣지의 네 꼭짓점 무게중심을 절단 기준점으로 사용합니다.
  접기 선을 만들 때 사용합니다.
  Args:
      e1_index: 첫 번째 엣지의 인덱스
      e2_index: 두 번째 엣지의 인덱스
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"
  
@mcp.tool()
def bisect(plane_co, plane_no) -> str:
  """
  지정한 점(plane_co)과 법선 벡터(plane_no)로 정의된 임의의 평면으로 메시 전체를 절단합니다.
  다른 접기 도구들이 내부적으로 사용하는 기본 절단 연산이며, 직접 호출도 가능합니다.
  접기 선을 만들 때 사용합니다.
  Args:
      plane_co: 절단 평면 위의 한 점 (x, y, z) 튜플 또는 벡터
      plane_no: 절단 평면의 법선 벡터 (x, y, z) 튜플 또는 벡터
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"

@mcp.tool()
def triangle_fold(v1_index, v2_index) -> str:
  """
  종이접기의 삼각형 접기(triangle fold)를 수행합니다.
  꼭짓점 v1의 인접 면들을 v1-v2 수직이등분선으로 절단한 뒤,
  v1을 새로 생성된 접기 선을 축으로 180° 회전하여 v2 위치로 접어 올립니다.
  Args:
      v1_index: 접어 올릴 꼭짓점의 인덱스 (이동되는 꼭짓점)
      v2_index: 목표 위치 꼭짓점의 인덱스
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"
  
@mcp.tool()
def icecream_fold(e1_index, e2_index) -> str:
  """
  종이접기의 아이스크림 접기(icecream fold / kite fold)를 수행합니다.
  두 엣지의 교점에서 각도 이등분선으로 메시를 절단한 후,
  엣지 e1의 꼭짓점들을 교점을 중심으로 180° 회전하여 이등분 접기 선 반대편으로 접습니다.
  Args:
      e1_index: 접힐 엣지의 인덱스 (이 엣지의 꼭짓점들이 이동됨)
      e2_index: 접기 기준이 되는 반대 엣지의 인덱스
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"

@mcp.tool()
def door_fold(e1_index, e2_index) -> str:
  """
  종이접기의 문 접기(door fold)를 수행합니다.
  두 엣지의 중간 지점에 평행한 선으로 메시를 절단하고,
  엣지 e1 및 그 인접 엣지의 꼭짓점들을 새 접기 선을 축으로 180° 회전합니다.
  Args:
      e1_index: 접힐 영역을 결정하는 엣지의 인덱스 (이 엣지 주변 꼭짓점들이 이동됨)
      e2_index: 접기 방향의 기준이 되는 반대 엣지의 인덱스
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"
  
@mcp.tool()
def reverse_fold(v_index, e_indices) -> str:
  """
  종이접기의 역접기(reverse fold)를 수행합니다.
  두 엣지(e_indices[0], e_indices[1])의 방향 평균으로 정의된 축을 기준으로
  꼭짓점 v를 180° 회전하여 레이어 사이로 접어 넣습니다.
  Args:
      v_index: 역접기를 적용할 꼭짓점의 인덱스
      e_indices: 접기 축을 정의하는 두 엣지 인덱스의 리스트 [e1_index, e2_index]
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"

@mcp.tool()
def v1v2_axis_fold(v_index, v1_index, v2_index, angle=math.pi) -> str:
  """
  두 꼭짓점(v1, v2)을 잇는 직선을 접기 축으로 하여 꼭짓점 v를 회전합니다.
  먼저 v 기준 접기 선 평면으로 메시를 절단한 후, 생성된 엣지를 축으로 v를 지정 각도만큼 회전합니다.
  Args:
      v_index: 회전시킬 꼭짓점의 인덱스
      v1_index: 접기 축의 시작 꼭짓점 인덱스
      v2_index: 접기 축의 끝 꼭짓점 인덱스
      angle: 회전 각도 (라디안, 기본값: math.pi = 180°)
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"

@mcp.tool()
def e_axis_fold(v_index, e_index, angle=math.pi) -> str:
  """
  기존 엣지(e)를 접기 축으로 하여 꼭짓점 v를 회전합니다.
  먼저 v 기준 접기 선 평면으로 메시를 절단한 후, 엣지 e 자체를 축으로 v를 지정 각도만큼 회전합니다.
  v1v2_axis_fold와 달리 새 교점 없이 기존 엣지를 직접 접기 축으로 사용합니다.
  Args:
      v_index: 회전시킬 꼭짓점의 인덱스
      e_index: 접기 축으로 사용할 엣지의 인덱스
      angle: 회전 각도 (라디안, 기본값: math.pi = 180°)
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"
  
@mcp.tool()
def rotate_v_around_e(v_index, e_index, angle=math.pi) -> str:
  """
  꼭짓점 v를 엣지 e의 축을 중심으로 지정된 각도만큼 회전합니다.
  메시 절단 없이 순수하게 꼭짓점의 위치만 변경합니다.
  이미 접힌 면의 꼭짓점 위치를 미세 조정하거나 날개 등을 펼치는 데 사용합니다.
  Args:
      v_index: 회전시킬 꼭짓점의 인덱스
      e_index: 회전 축으로 사용할 엣지의 인덱스
      angle: 회전 각도 (라디안, 기본값: math.pi = 180°)
  Returns:
      작업 완료 메시지 "done"
  """
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
  
  return f"done"