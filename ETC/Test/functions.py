import bpy
import math
from mathutils import Vector


################# setting && init ####################

def init_objects_data():
    for id_data in bpy.data.objects:
        bpy.data.objects.remove(id_data)


def single_vert_setting():
  bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
        

def pivot_setting():
  bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'


def create_new_plane(newName='newObj'):      # name 이란 이름의 plane생성
  bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
  curObj=bpy.context.active_object
  curObj.name=newName

  return curObj # return 값은 전역변수에 활용할것
  

################### info ######################

def edge_to_vertex_index(curObj, edgeIndex):

  result = []

  for vertexIndex in curObj.data.edges[edgeIndex].vertices: # edge의 vertices는 항상 2개
    result.append(vertexIndex)
  
  return result


def edge_to_unit_vector(curObj, edgeIndex):
  vertexIndex = edge_to_vertex_index(curObj, edgeIndex)
  p1 = curObj.data.vertices[vertexIndex[0]].co  # (x1, y1, z1) # Vector class
  p2 = curObj.data.vertices[vertexIndex[1]].co  # (x2, y2, z2)
  v = p2-p1
  
  v_len = math.sqrt(v.x**2+v.y**2+v.z**2) # v_len = v.length
  u = v/(v_len) # u = v.normalized()
  
  return u


def set_select_value(curObj, vertexIndex=None, edgeIndex=None, setValue = True):

  bpy.ops.object.mode_set(mode = 'OBJECT')

  #### vertex ####
  vertexInputType = type(vertexIndex)

  if vertexInputType is int:
    curObj.data.vertices[vertexIndex].select = setValue
  elif vertexInputType is list:
    for i in vertexIndex:
      curObj.data.vertices[i].select = setValue
  
  #### edge ####
  edgeInputType = type(edgeIndex)

  if edgeInputType is int:
    curObj.data.edges[edgeIndex].select = setValue
  elif edgeInputType is list:
    for i in edgeIndex:
      curObj.data.edges[i].select = setValue

  #### Edit 모드 진입 후 선택 확인 ####
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_mode(type="VERT")


def deselect_all():
  if bpy.context.active_object is not None:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

def select_all():
  if bpy.context.active_object is not None:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')



def select_additional(curObj, vertexIndex=None, edgeIndex=None):
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=True)


def select_only(curObj, vertexIndex=None, edgeIndex=None):
  deselect_all(curObj)
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=True)


def deselect(curObj, vertexIndex=None, edgeIndex=None): # 동작안함
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=False)


################ transform ######################

def translate_all_vertex(vector3):

  if type(vector3) is Vector:
    if len(vector3) == 3:
      pass
  elif type(vector3) is tuple or type(vector3) is list:
    if len(vector3) == 3:
      vector3 = Vector(vector3)
  else:
    return

  x=vector3.x
  y=vector3.y
  z=vector3.z

  # TODO 현재 선택되어있는 vertex list로 생성
  select_all() # Edit 모드 상태
  bpy.ops.transform.translate(value=(x, y, z))
  # TODO 선택되어있던 vertex list대로 다시 선택  

def rotate(value=3.141592):
  bpy.ops.transform.rotate(value=value, orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')


def rotate_specific_line():
    # 두 점의 좌표 알기, 해당 벡터 알기
    # TODO
    print('hi')

init_objects_data()
curObj = create_new_plane()
select_only(curObj, vertexIndex=0)
deselect(curObj, vertexIndex=0)