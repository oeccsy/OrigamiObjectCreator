import bpy
import math
from mathutils import Vector
import numpy as np
import os

from Modules.blenderControl import *
from Modules.calculate import *


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


def reflection_about_vertex(curObj, vertexIndex, vertexIndex_midpoint):
  m=curObj.data.vertices[vertexIndex_midpoint].co
  p=curObj.data.vertices[vertexIndex].co

  select_only(curObj, vertexIndex=vertexIndex)
  translate((m-p+m-p))


'''
def reflection_about_vertices(curObj, vertexIndex, vertexIndexList):
  # 방법3. edge 직접 구해서 대칭 (각 성분 이동, translate 이용)
  p1=curObj.data.vertices[vertexIndexList[0]].co
  p2=curObj.data.vertices[vertexIndexList[1]].co
  locus = find_locus(p1, p2)
  p=curObj.data.vertices[vertexIndex].co

  h=find_point_H(p, locus)

  translate((h-p) * 2)
'''

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