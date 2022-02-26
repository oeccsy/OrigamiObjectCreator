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

  reflection_about_vertex(curObj, vertexIndex=3, vertexIndex_midpoint=13) #대칭은 되지만 완벽한 대칭은 실제 종이접기와 다름

  #fbx_export()