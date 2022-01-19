import bpy
import math
from mathutils import Vector
import numpy as np
import os

################# setting && init ####################

def bpy_version_check():
  print(bpy.app.version_string)


def init_objects_data():
    for id_data in bpy.data.objects:
        bpy.data.objects.remove(id_data)


def single_vert_setting(): # 해당 함수 호출 시 single_vert 사용 가능
  bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
        

def pivot_setting(): # rotate가 CURSOR를 기준으로 동작하지 않아서 사용안함
  bpy.ops.object.mode_set(mode='EDIT')
  previous_context = bpy.context.area.type
  
  bpy.context.area.type = 'VIEW_3D'
  bpy.ops.view3d.snap_cursor_to_center() # 3d커서를 원점으로 이동
  bpy.data.scenes["Scene"].tool_settings.transform_pivot_point = 'CURSOR'
  
  bpy.context.area.type = previous_context


def create_new_plane(newName='newObj'):      # name 이란 이름의 plane생성
  bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
  curObj=bpy.context.active_object
  curObj.name=newName

  return curObj # return 값은 전역변수에 활용할것
  
  
def update_object_data():
  bpy.ops.object.mode_set(mode='OBJECT')
  bpy.ops.object.mode_set(mode='EDIT')
    
    
################### info ######################

def vertex_pos(curObj, vertexIndex):
    return curObj.data.vertices[vertexIndex].co.copy() # .co로 return 하는 경우 얕은복사 .copy()로 return 하는 경우 깊은복사


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
  deselect_all()
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=True)


def deselect(curObj, vertexIndex=None, edgeIndex=None): # 동작안함
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=False)


######## control ########

def subdivide():
  bpy.ops.mesh.subdivide()
  update_object_data()
  # Editmode가 아닌 경우 error 발생


def connect_selected():
  bpy.ops.mesh.vert_connect_path()
  update_object_data()


def fbx_export(name='newObj'):
  bpy.ops.export_scene.fbx(filepath=str(os.path.dirname(os.path.realpath(__file__)))+ "\\..\\Output\\" + name+".fbx", object_types={'MESH'}, use_mesh_modifiers=False, add_leaf_bones=False, bake_anim=False)