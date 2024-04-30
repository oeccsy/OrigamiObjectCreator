import bpy
import bmesh
import math
import mathutils


### obj 선택

def select_obj(name="NewObj"):
  bpy.data.objects[name].select_set(True)
  return bpy.data.objects[name]
  
# active_object는 단일 오브젝트를 나타내고,
# selected_objects는 여러 오브젝트의 목록을 나타낸다.

# 만약 사용자가 하나의 오브젝트만 선택한 경우
# active_object 와 selected_objects 는 동일한 오브젝트를 나타낸다.

# 여러 오브젝트가 선택된 경우
# active_object는 마지막으로 선택된 오브젝트를 나타내고,
# selected_objects는 모든 선택된 오브젝트의 목록을 나타낸다.
  
def get_active_obj():
  return bpy.context.active_object

def get_selected_objs():
  return bpy.context.selected_objects


### vertex / edge 선택
# bmesh 모듈을 이용
# bmesh : 복잡한 메시 조작 작업을 수행하는 데 사용하는 모듈

def select_vertices(index_list=[]):
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
  
  # 엣지 선택
  selected_verts = []
  
  for index in index_list:
    bm.verts[index].select_set(True)
    selected_verts.append(selected_verts)

  # 변경된 선택 사항을 메시에 적용
  bmesh.update_edit_mesh(obj.data)
  
  # 메모리 해제
  bm.free()
  
  return selected_verts
  

def select_edges(index_list=[]):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.context.tool_settings.mesh_select_mode = (False, True, False)
  bpy.ops.mesh.select_all(action='DESELECT')
  
  # 메시 데이터를 수정하기 위해 bmesh 불러오기
  bm = bmesh.from_edit_mesh(obj.data)
  
  # 모든 선택 해제
  bm.select_flush(False)
  bm.edges.ensure_lookup_table()
  
  # 엣지 선택
  selected_edges = []
  
  for index in index_list:
    bm.edges[index].select = True
    selected_edges.append(bm.edges[index])

  #변경된 선택 사항을 메시에 적용
  bmesh.update_edit_mesh(obj.data)
  
  # 메모리 해제
  bm.free()
  
  return selected_edges
  
  
def select_faces(index_list=[]):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.context.tool_settings.mesh_select_mode = (False, False, True)
  bpy.ops.mesh.select_all(action='DESELECT')
  
  # 메시 데이터를 수정하기 위해 bmesh 불러오기
  bm = bmesh.from_edit_mesh(obj.data)
  
  # 모든 선택 해제fro
  bm.select_flush(False)
  bm.faces.ensure_lookup_table()
  
  # 엣지 선택
  selected_faces = []
  
  for index in index_list:
    bm.faces[index].select = True
    selected_faces.append(bm.faces[index])

  #변경된 선택 사항을 메시에 적용
  bmesh.update_edit_mesh(obj.data)
  
  # 메모리 해제
  bm.free()
  
  return selected_faces
  

### subdivide
def subdivide_edges(index_list=[]):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.context.tool_settings.mesh_select_mode = (True, False, False)
  bpy.ops.mesh.select_all(action='DESELECT')
  
  # 메시 데이터를 수정하기 위해 bmesh 불러오기
  bm = bmesh.from_edit_mesh(obj.data)
  
  # 모든 선택 해제
  bm.select_flush(False)
  bm.edges.ensure_lookup_table()
  
  selected_edges = []

  # 엣지 선택
  for index in index_list:
    bm.edges[index].select_set(True)
    selected_edges.append(bm.edges[index])

  bmesh.ops.subdivide_edges(bm,
                            edges=selected_edges,
                            cuts=1,
                            use_grid_fill=True,
                            )     
  
  # 변경된 선택 사항을 메시에 적용
  bmesh.update_edit_mesh(obj.data)
  
  # 메모리 해제
  bm.free()
  

def subdivide_edge(index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object

  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='DESELECT')
  bpy.context.tool_settings.mesh_select_mode = (True, False, False)

  bm = bmesh.from_edit_mesh(obj.data)

  bm.select_flush(False)
  bm.edges.ensure_lookup_table()

  bm.edges[index].select_set(True)
  bmesh.update_edit_mesh(obj.data) 

  bmesh.ops.subdivide_edges(bm,
                            edges=[bm.edges[index]],
                            cuts=1,
                            use_grid_fill=True,
                            )                          
  bmesh.update_edit_mesh(obj.data) 
  bm.free()

def get_vert_vec(index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  return obj.data.vertices[index].co

def get_edge_vec(index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object

  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='DESELECT')
  bpy.context.tool_settings.mesh_select_mode = (True, False, False)

  bm = bmesh.from_edit_mesh(obj.data)

  bm.select_flush(False)
  bm.edges.ensure_lookup_table()
  
  bm.edges[index].select_set(True)
  bmesh.update_edit_mesh(obj.data) 
  
  edge = bm.edges[index]
  v1 = edge.verts[0].co
  v2 = edge.verts[1].co
  
  bm.free()
  
  return v2 - v1


def get_face_normal(index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  return obj.data.polygons[index].normal


def get_face_center(index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object
  return obj.data.polygons[index].center


def rotation_matrix(axis, theta): # 로드리게스 회전, 반시계 방향으로 회전
    axis.normalize()
    a, b, c = axis
    
    I = mathutils.Matrix.Identity(3)
    K = mathutils.Matrix([[0, -c, b],
                          [c, 0, -a],
                          [-b, a, 0]])
    R = I + math.sin(theta) * K + (1 - math.cos(theta)) * K @ K
    
    return R

def rotate_with_matrix(R, index):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  obj = bpy.context.active_object

  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='DESELECT')
  bpy.context.tool_settings.mesh_select_mode = (True, False, False)

  bm = bmesh.from_edit_mesh(obj.data)

  bm.select_flush(False)
  bm.edges.ensure_lookup_table()
  
  bm.edges[index].select_set(True)
  bmesh.update_edit_mesh(obj.data) 
  
  edge = bm.edges[index]
  for vert in edge.verts:
      vert.co = R @ vert.co
  
  bm.free()    

def bisect():
  bpy.ops.mesh.bisect(plane_co=(0.0, 0.0, 0.0), plane_no=(1.0, 0.0, 0.0), use_fill=False, clear_inner=False, clear_outer=False, threshold=0.0001, xstart=10, xend=-10, ystart=10, yend=-10)
  
#subdivide_edges([0,2])

#select_edges([3])
#axis = get_edge_vec(6)

#print(axis)

# 회전 행렬 생성
#R = mathutils.Matrix.Rotation(math.pi * 0.99, 3, axis)

#rotate_with_matrix(R, 3)