from Modules import *

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

  fbx_export()