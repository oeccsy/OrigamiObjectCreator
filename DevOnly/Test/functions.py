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


def single_vert_setting():
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

'''
def is_vector3(vector3):
  if type(vector3) is Vector:
    if len(vector3) == 3:
      pass
  elif type(vector3) is tuple or type(vector3) is list:
    if len(vector3) == 3:
      vector3 = Vector(vector3)
  else:
    print("[is_vector3] : no vector")
    return False
  
  return True
'''


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
  bpy.ops.transform.translate(value=(x, y, z)) # Translate가 아닌 position에 행렬을 곱하는 형태로 구현해보기
  T=np.array(
    [[1, 0, 0, -x],
    [0, 1, 0, -y],
    [0, 0, 1, -z],
    [0, 0, 0, 1]]
  )
  # TODO 선택되어있던 vertex list대로 다시 선택
  update_object_data()


def rotate_X(radian=0): # counterclockwise로 동작하기 위해 value에 음의 값 부여
  bpy.ops.transform.rotate(value=-radian, orient_axis='X', center_override=(0,0,0))
  update_object_data()


def rotate_Y(radian=0):
  bpy.ops.transform.rotate(value=-radian, orient_axis='Y', center_override=(0,0,0))
  update_object_data()


def rotate_Z(radian=0):
  bpy.ops.transform.rotate(value=-radian, orient_axis='Z', center_override=(0,0,0))
  update_object_data()


def rotate_vector_to_planeXY(vector3): # vector3 하나를 입력받는다. ex) (a, b, c)

  vector_on_xz=Vector((vector3.x, 0, vector3.z))  # xz평면으로의 정사영 벡터를 찾는다. ex) (a, 0, c)
  vector_x=Vector((1,0,0))

  cos_theta=vector_on_xz.dot(vector_x)/vector_on_xz.length/vector_x.length  # 해당 벡터와 x축 사이의 cos값을 구한다.
  theta=math.acos(cos_theta)  # cos 값을 통해 해당 벡터와 y축 사이의 각을 구한다.

  if vector3.z > 0: # 구한 각이 반시계 방향으로의 각인지 확인한다. 
    rotate_Y(theta) # y축을 기준으로 회전하여 xy평면 위에 위치시킨다.
  else:
    theta = 2*math.pi - theta
    rotate_Y(theta)

  return theta
  
    
def rotate_vector_to_planeYZ(vector3):

  vector_on_xy=Vector((vector3.x, vector3.y, 0))  # xy평면으로의 정사영
  vector_y=Vector((0,1,0))

  cos_theta=vector_on_xy.dot(vector_y)/vector_on_xy.length/vector_y.length  # 해당 벡터와 y축 사이의 cos값을 구한다.
  theta=math.acos(cos_theta)  # cos 값 -> 사이의 각

  if vector3.x > 0: # z축을 기준으로 회전하여 xz평면 위에 위치시킨다.
    rotate_Z(theta)
  else:
    theta = 2*math.pi - theta
    rotate_Z(theta)
  
  return theta

    
def rotate_vector_to_planeXZ(vector3):

  vector_on_yz=Vector((0, vector3.y, vector3.z))  # yz평면으로의 정사영
  vector_z=Vector((0,0,1))

  cos_theta=vector_on_yz.dot(vector_z)/vector_on_yz.length/vector_z.length  # 해당 벡터와 z축 사이의 cos값을 구한다.
  theta=math.acos(cos_theta)  # cos 값 -> 사이의 각

  if vector3.y > 0: # x축을 기준으로 회전하여 xz평면 위에 위치시킨다.
    rotate_X(theta)
  else:
    theta = 2*math.pi - theta
    rotate_X(theta)

  return theta


def rotate_around_edge(curObj, vertexIndex, edgeIndex, angle): # 회전시킬 vertex list, 회전할 축 받아오기
    
    # edge를 이루는 한 vertex의 좌표 알기
    vertexIndex_of_edge=edge_to_vertex_index(curObj, edgeIndex)
    p1=vertex_pos(curObj, vertexIndex_of_edge[0])
    
    # 해당 벡터가 원점을 지나도록 translate해주기 (p1이 원점에 오도록 translate)
    print(p1)
    translate_all_vertex(-p1)

    # rotation 하여 z축 위에 벡터가 오도록 해주기
    edgeVector=edge_to_unit_vector(curObj, edgeIndex)
    angleZ=rotate_vector_to_planeYZ(edgeVector)
    edgeVector=edge_to_unit_vector(curObj, edgeIndex) # rotate 이후 벡터가 바뀐것을 반영해야함
    angleX=rotate_vector_to_planeXZ(edgeVector)

    # z축을 기준으로 vertex들을 rotate 해주기
    select_only(curObj, vertexIndex=vertexIndex)
    rotate_Z(angle)

    # z축으로 옮겼던 축을 기존 상태로 복구
    select_all()
    rotate_X(-angleX)
    rotate_Z(-angleZ)

    # 다시 p1만큼 translate 해주기
    print(p1)
    translate_all_vertex(p1)
    
    # 복구 완료

############## 추가 작성 ###############

def translate_edge_to_origin(curObj, edgeIndex):
  # edge를 이루는 한 vertex의 좌표 알기
  vertexIndex_of_edge=edge_to_vertex_index(curObj, edgeIndex)
  p1=vertex_pos(curObj, vertexIndex_of_edge[0])
    
  # 해당 벡터가 원점을 지나도록 translate해주기 (p1이 원점에 오도록 translate)
  translate_all_vertex(-p1)


def rotate_edge_to_axisX(curObj, edgeIndex):
  translate_edge_to_origin(curObj, edgeIndex)
  rotate_vector_to_planeXZ()

def reflection_about_edge(curObj, vertexIndex, edgeIndex):
  # 방법1.
  # edge를 x축 위에 위치시킴
  # reflection할 vertex를 xz평면에 위치시킴
  # xy평면을 이용하여 대칭이동 -> z좌표의 부호 변경
  # vertex가 여러개일 경우 비효율

  # 방법2. edge 직접 구해서 대칭 (각 성분 이동, translate 이용)

  # 방법3. edge에 대하여 pi 만큼 rotate
  rotate_around_edge(curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, angle=math.pi)


def internal_division(curObj, v1_index, v2_index, ratio):
  # subdivide()
  # 버텍스 정보를 가져옴
  # 내분점 계산
  # 차이만큼 translate
  # TODO
  print("todo")




######## control ########

def subdivide():
  bpy.ops.mesh.subdivide()
  update_object_data()
  # Editmode가 아닌 경우 error 발생


def connect_selected():
  bpy.ops.mesh.vert_connect_path()
  update_object_data()


def fbx_export(name='newObj'):
  bpy.ops.export_scene.fbx(filepath=str(os.path.dirname(os.path.realpath(__file__)))+ "\\" + name+".fbx", object_types={'MESH'}, use_mesh_modifiers=False, add_leaf_bones=False, bake_anim=False)


init_objects_data()
curObj = create_new_plane()
select_only(curObj, vertexIndex=[0,3])
connect_selected()




select_only(curObj, vertexIndex=[1,3])
subdivide()
select_only(curObj, vertexIndex=[0,2])
subdivide()
select_only(curObj, vertexIndex=[4,5])
connect_selected()
select_only(curObj, vertexIndex=[2,3])
rotate_X(0.74)
subdivide()
select_only(curObj, vertexIndex=[6,4])
connect_selected()
select_all()

rotate_around_edge(curObj, vertexIndex=3, edgeIndex=8, angle=math.pi)