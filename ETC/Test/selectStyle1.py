import bpy

def select_additional(curObj, vertexIndex=None, edgeIndex=None):
  bpy.ops.object.mode_set(mode = 'OBJECT')
  
  #### vertex 선택 ####
  vertexInputType = type(vertexIndex)

  if vertexInputType == int:
    curObj.data.vertices[vertexIndex].select = True

  elif vertexInputType == list:
    for i in vertexIndex:
      curObj.data.vertices[i].select = True
  
  #### edge 선택 ####
  edgeInputType = type(edgeIndex)

  if edgeInputType == int:
    curObj.data.edges[edgeIndex].select = True
  
  elif edgeInputType == list:
    for i in edgeIndex:
      curObj.data.edges[i].select = True

  #### Edit 모드 진입 후 선택 확인 ####
  
  bpy.ops.object.mode_set(mode = 'EDIT')
  bpy.ops.mesh.select_mode(type="VERT")


def select_only(curObj, vertexIndex=None, edgeIndex=None):

  #### 기존 mesh 선택 해제 ####
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action = 'DESELECT')  # 기존 mesh 선택 해제

  #### 선택 ####
  select_additional(curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex)



