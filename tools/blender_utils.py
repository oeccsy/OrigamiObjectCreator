from mcp_instance import mcp
import bpy
import os
import json
import bmesh

@mcp.tool()
def bpy_version_check() -> str:
  print(bpy.app.version_string)
  return f"bpy version : {bpy.app.version_string}"

@mcp.tool()
def init_objects_data() -> str:
    for id_data in bpy.data.objects:
        bpy.data.objects.remove(id_data)
    
    return f"init done"
        
@mcp.tool()
def create_new_plane(name='plane') -> str:      
  bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0), scale=(1, 1, 1))

  cur_obj=bpy.context.active_object
  cur_obj.name=name

  return f"create plane done, name : {name}"

@mcp.tool()
def get_mesh_data() -> str:
    obj = bpy.context.active_object

    if obj.mode == 'EDIT':
        bm = bmesh.from_edit_mesh(obj.data)
    else:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
    
    vertices = [[v.co.x, v.co.y, v.co.z] for v in bm.verts]
    edges = [[e.verts[0].index, e.verts[1].index] for e in bm.edges]
    faces = [[v.index for v in f.verts] for f in bm.faces]
    
    if obj.mode != 'EDIT':
        bm.free()
    
    return json.dumps({
      "vertices": vertices,
      "edges": edges,
      "faces": faces
    })

@mcp.tool()
def save() -> str:
  """
  현재 blender 프로젝트를 정해진 경로에 저장합니다.
  """
  save_dir = str(os.path.dirname(os.path.realpath(__file__))) + "\\..\\output\\"
  os.makedirs(save_dir, exist_ok=True)
  
  save_path = os.path.join(save_dir, "project.blend")
  save_path = os.path.abspath(save_path)
  
  bpy.ops.wm.save_as_mainfile(filepath=save_path)
  print(f"Saved to: {save_path}")
  
  return f"Saved to: {save_path}"

@mcp.tool()
def fbx_export(name='result') -> str:
  export_path = str(os.path.dirname(os.path.realpath(__file__))) + "\\..\\output\\" + name + ".fbx"
  bpy.ops.export_scene.fbx(filepath=export_path, object_types={'MESH'}, use_mesh_modifiers=False, add_leaf_bones=False, bake_anim=False)
  
  return f"export done, path : {export_path}"
  
@mcp.tool()
def stl_export(name='result') -> str:
  export_path = str(os.path.dirname(os.path.realpath(__file__))) + "\\..\\output\\" + name + ".stl"
  bpy.ops.export_mesh.stl(filepath=export_path)
  
  return f"export done, path : {export_path}"