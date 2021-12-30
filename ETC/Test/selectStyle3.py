import bpy

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
  bpy.ops.object.mode_set(mode = 'EDIT')
  bpy.ops.mesh.select_mode(type="VERT")


def all_deselect(curObj):
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_all(action = 'DESELECT')


def select_additional(curObj, vertexIndex=None, edgeIndex=None):
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=True)


def select_only(curObj, vertexIndex=None, edgeIndex=None):
  all_deselect(curObj)
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=True)


def deselect(curObj, vertexIndex=None, edgeIndex=None):
  set_select_value(curObj=curObj, vertexIndex=vertexIndex, edgeIndex=edgeIndex, setValue=False)