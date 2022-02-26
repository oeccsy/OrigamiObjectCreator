from Modules import *

def create_paperairplane():

  init_objects_data()
  curObj = create_new_plane()
  select_only(curObj, vertexIndex=[0,3])
  connect_selected()

  

  #fbx_export()