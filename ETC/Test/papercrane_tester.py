import bpy
import math
import os
from mathutils import Vector
import numpy as np
import sympy as sp

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


def select_new_vertex():
  curObj=bpy.context.active_object
  update_object_data()
  newVertexIndex=len(curObj.data.vertices)-1
  select_only(curObj, vertexIndex=newVertexIndex)

  return newVertexIndex


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




### 선분p1p2를 a:b로 내분 ###
def internal_division(p1, p2, a, b):
  vector_p1p2 = p2-p1
  k = a / (a+b)

  return p1 + vector_p1p2 * k

### 직선의 자취 ###
def find_locus(p1, p2):
  u=(p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]) #방향 벡터
  t=sp.Symbol('t')
  result = (u[0]*t+p1[0], u[1]*t+p1[1], u[2]*t+p1[2])
  print("hi")
  return result

### 점에서 직선에 내린 수선의 발 ###
def find_point_H(point, line):
  t=sp.Symbol('t')

  u=tuple(i.subs({t: 0}) - i.subs({t: 1}) for i in line) # 직선의 방향벡터
  n=tuple(p-l for p, l in zip(point, line)) # 수선의 발 벡터

  #dot_product=sum([uv*nv for uv, nv in zip(u, n)])
  dot_product=u[0]*n[0] + u[1]*n[1] + u[2]*n[2]
  
  value = sp.solveset(dot_product, t) #해를 찾는다.
  
  value0=float(value.args[0]) #value는 sympy의 FiniteSet

  result=tuple(i.subs({t: value0}) for i in line) # line(tuple)에 t=value0 대입

  return result



################ transform ######################

def translate(vector3):
  if type(vector3) is Vector:
    if len(vector3) == 3:
      pass
    else:
      raise
  elif type(vector3) is tuple or type(vector3) is list:
    if len(vector3) == 3:
      vector3 = Vector(vector3)
    else:
      raise TypeError

  x=vector3.x
  y=vector3.y
  z=vector3.z

  bpy.ops.transform.translate(value=(x, y, z))


def translate_all_vertex(vector3):

  if type(vector3) is Vector:
    if len(vector3) == 3:
      pass
  elif type(vector3) is tuple or type(vector3) is list:
    if len(vector3) == 3:
      vector3 = Vector(vector3)

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


######## 임의의 벡터를 xyz 평면 위로 rotate ########


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


###### 특정 edge에 대하여 rotate ######

def rotate_around_edge(curObj, vertexIndex, edgeIndex, angle): # 회전시킬 vertex list, 회전할 축 받아오기
    
    # edge를 이루는 한 vertex의 좌표 알기
    vertexIndex_of_edge=edge_to_vertex_index(curObj, edgeIndex)
    p1=vertex_pos(curObj, vertexIndex_of_edge[0])
    
    # 해당 벡터가 원점을 지나도록 translate해주기 (p1이 원점에 오도록 translate)
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

  # 방법2. edge에 대하여 pi 만큼 rotate
  rotate_around_edge(curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, angle=math.pi)


def reflection_about_vertex(curObj, vertexIndex, vertexIndex_midpoint): # 대칭은 되지만 완벽한 대칭은 실제 종이접기와 다름
  m=curObj.data.vertices[vertexIndex_midpoint].co
  p=curObj.data.vertices[vertexIndex].co

  select_only(curObj, vertexIndex=vertexIndex)
  translate((m-p+m-p))


def reflection_about_vertices(curObj, vertexIndex, vertexIndexList):
  # 방법3. edge 직접 구해서 대칭 (각 성분 이동, translate 이용)
  p1=curObj.data.vertices[vertexIndexList[0]].co
  p2=curObj.data.vertices[vertexIndexList[1]].co
  locus = find_locus(p1, p2)
  p=curObj.data.vertices[vertexIndex].co

  h=find_point_H(p, locus)

  translate((h-p) * 2)


def create_vertex_h(curObj, vertexIndex, edgeIndex):

  indexlist=edge_to_vertex_index(curObj,edgeIndex)
  p1=tuple(curObj.data.vertices[indexlist[0]].co)
  p2=tuple(curObj.data.vertices[indexlist[1]].co)

  p=tuple(curObj.data.vertices[vertexIndex].co)
  locus=find_locus(p1,p2)  
  h=Vector(find_point_H(p, locus))

  select_only(curObj, vertexIndex=indexlist)
  subdivide()
  hIndex=select_new_vertex()
  cur_h_co=curObj.data.vertices[hIndex].co

  translate(h-cur_h_co)


def angle_bisector(curObj, vertexIndex):

  if len(vertexIndex) != 3:
    raise

  # vertex정보 가져옴
  p1 = curObj.data.vertices[vertexIndex[0]].co
  p2 = curObj.data.vertices[vertexIndex[1]].co
  p3 = curObj.data.vertices[vertexIndex[2]].co

  # 내분점 계산
  p1p2_length = (p2-p1).length
  p2p3_length = (p3-p2).length
  target_pos=internal_division(p1, p3, p1p2_length, p2p3_length)

  # 새로운 vertex 생성
  select_only(curObj=curObj,vertexIndex=[vertexIndex[0], vertexIndex[2]])
  subdivide()
  select_new_vertex()
  
  # 해당 위치로 translate
  value = target_pos-curObj.data.vertices[len(curObj.data.vertices)-1].co
  translate(value)

  select_additional(curObj, vertexIndex[1])
  connect_selected()


def create_papercrane():

  init_objects_data()
  curObj = create_new_plane()
  select_only(curObj, vertexIndex=[0,3])
  connect_selected()

  rotate_around_edge(curObj, vertexIndex=1, edgeIndex=4, angle=-math.pi+0.03)

  select_only(curObj, vertexIndex=[0,3])
  subdivide()

  select_only(curObj, vertexIndex=[1,4])
  connect_selected()

  select_only(curObj, vertexIndex=[1,3])
  subdivide()
  select_only(curObj, vertexIndex=[2,3])
  subdivide()

  select_only(curObj, vertexIndex=[4,5])
  connect_selected()
  select_only(curObj, vertexIndex=[4,6])
  connect_selected()

  rotate_around_edge(curObj, vertexIndex=3, edgeIndex=9, angle=math.pi-0.03)
  rotate_around_edge(curObj, vertexIndex=5, edgeIndex=4, angle=math.pi)

  select_only(curObj, vertexIndex=[0,2])
  subdivide()
  select_only(curObj, vertexIndex=[4,7])
  connect_selected()
  select_only(curObj, vertexIndex=[0,1])
  subdivide()
  select_only(curObj, vertexIndex=[4,8])
  connect_selected()

  rotate_around_edge(curObj, vertexIndex=0, edgeIndex=12, angle=math.pi-0.03)
  rotate_around_edge(curObj, vertexIndex=7, edgeIndex=5, angle=math.pi)

  angle_bisector(curObj, [5,3,4])
  angle_bisector(curObj, [5,1,4])
  reflection_about_edge(curObj, vertexIndex=5, edgeIndex=17)
  
  angle_bisector(curObj, [6,3,4])
  angle_bisector(curObj, [6,2,4])
  reflection_about_edge(curObj, vertexIndex=6, edgeIndex=20)
  
  angle_bisector(curObj, [7,0,4])
  angle_bisector(curObj, [7,2,4])
  reflection_about_edge(curObj, vertexIndex=7, edgeIndex=23)
  
  angle_bisector(curObj, [8,0,4])
  angle_bisector(curObj, [8,1,4])
  reflection_about_edge(curObj, vertexIndex=8, edgeIndex=26)
  
  create_vertex_h(curObj, vertexIndex=9, edgeIndex=4)
  select_only(curObj, vertexIndex=[9,13])
  connect_selected()
  select_only(curObj, vertexIndex=[10,13])
  connect_selected()

  #reflection_about_vertex(curObj, vertexIndex=3, vertexIndex_midpoint=13)
  rotate_around_edge(curObj, vertexIndex=3, edgeIndex=29, angle=math.pi+0.1)
  rotate_around_edge(curObj, vertexIndex=6, edgeIndex=29, angle=math.pi+0.1)
  rotate_around_edge(curObj, vertexIndex=5, edgeIndex=29, angle=math.pi+0.1) # 연결된 점도 같이 대칭되어야 모양이 나옴

  create_vertex_h(curObj, vertexIndex=12, edgeIndex=5)
  select_only(curObj, vertexIndex=[11,14])
  connect_selected()
  select_only(curObj, vertexIndex=[12,14])
  connect_selected()
  
  rotate_around_edge(curObj, vertexIndex=0, edgeIndex=32, angle=math.pi-0.1)
  rotate_around_edge(curObj, vertexIndex=7, edgeIndex=32, angle=math.pi-0.1)
  rotate_around_edge(curObj, vertexIndex=8, edgeIndex=32, angle=math.pi-0.1)

  #9번 vertex와 연결된 모든 edge를 subdivide 해야함
  #fbx_export()

  #fbx_export()