import bpy

def select_base_func(curObj, vertexIndex=None, edgeIndex=None, isSelectOnly=True, isSelect=True):

  ######## isSelectOnly == True 일 경우 기존 mesh 선택 해제 ########

  if isSelectOnly == True:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')


  ######## isSelect == True일 경우 선택 False일 경우 선택해제 ########

  bpy.ops.object.mode_set(mode = 'OBJECT')
  
  #### vertex ####
  vertexInputType = type(vertexIndex)

  if vertexInputType == int:
    curObj.data.vertices[vertexIndex].select = isSelect

  elif vertexInputType == list:
    for i in vertexIndex:
      curObj.data.vertices[i].select = isSelect
  
  #### edge ####
  edgeInputType = type(edgeIndex)

  if edgeInputType == int:
    curObj.data.edges[edgeIndex].select = isSelect
  
  elif edgeInputType == list:
    for i in edgeIndex:
      curObj.data.edges[i].select = isSelect

  #### Edit 모드 진입 후 선택 확인 ####
  
  bpy.ops.object.mode_set(mode = 'EDIT')
  bpy.ops.mesh.select_mode(type="VERT")


def select_additional(curObj, vertexIndex=None, edgeIndex=None):
  select_base_func(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, isSelectOnly=False, isSelect=True)

def select_only(curObj, vertexIndex=None, edgeIndex=None):
  select_base_func(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, isSelectOnly=True, isSelect=True)

def deselect(curObj, vertexIndex=None, edgeIndex=None):
  select_base_func(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, isSelectOnly=False, isSelect=False)