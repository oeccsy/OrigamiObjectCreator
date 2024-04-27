import bpy
import bmesh

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
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='DESELECT')
  bpy.context.tool_settings.mesh_select_mode = (True, False, False)
  
  # 메시 데이터를 수정하기 위해 bmesh 불러오기
  bm = bmesh.from_edit_mesh(obj.data)
  
  # 모든 선택 해제
  bm.select_flush(False)
  
  # 엣지 선택
  for index in index_list:
    bm.verts[index].select_set(True)

  # 변경된 선택 사항을 메시에 적용
  bmesh.update_edit_mesh(obj.data)
  
  # 메모리 해제
  bm.free()
  
  bpy.ops.object.mode_set(mode='OBJECT')
  

def select_edge(index_list=[]):
  obj = bpy.context.active_object
  
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action='DESELECT')
  
  # 메시 데이터를 수정하기 위해 bmesh 불러오기
  bm = bmesh.from_edit_mesh(obj.data)
  bpy.context.tool_settings.mesh_select_mode = (False, True, False)
  
  # 모든 선택 해제
  bm.select_flush(False)
  
  # 엣지 선택
  for index in index_list:
    bm.edges[index].select = True

# 변경된 선택 사항을 메시에 적용
  bmesh.update_edit_mesh(obj.data)
  
  # 메모리 해제
  bm.free()
  
  bpy.ops.object.mode_set(mode='OBJECT')
  
  