import Models
import Modules

if __name__ == '__main__':
  Modules.blender_utils.init_objects_data()
  Modules.blender_utils.create_new_plane()
  Models.create_papercrane()
  Modules.blender_utils.fbx_export("paper_crane")    
