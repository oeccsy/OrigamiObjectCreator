import bpy
import os

def bpy_version_check():
  print(bpy.app.version_string)


def init_objects_data():
    for id_data in bpy.data.objects:
        bpy.data.objects.remove(id_data)
        

def create_new_plane(name='plane'):      
  bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0), scale=(1, 1, 1))

  cur_obj=bpy.context.active_object
  cur_obj.name=name

  return cur_obj
  

def fbx_export(name='result'):
  bpy.ops.export_scene.fbx(filepath=str(os.path.dirname(os.path.realpath(__file__))) + "\\..\\Output\\" + name + ".fbx", object_types={'MESH'}, use_mesh_modifiers=False, add_leaf_bones=False, bake_anim=False)
  
def stl_export(name='result'):
  bpy.ops.export_mesh.stl(filepath=str(os.path.dirname(os.path.realpath(__file__))) + "\\..\\Output\\" + name + ".stl")