from mcp_instance import mcp
import bpy
import os
import json
import bmesh

@mcp.tool()
def bpy_version_check() -> str:
  """
  현재 실행 중인 Blender Python API(bpy)의 버전을 확인합니다.
  Returns:
      bpy 버전 정보 문자열 (예: "bpy version : 4.1.0")
  """
  print(bpy.app.version_string)
  return f"bpy version : {bpy.app.version_string}"

@mcp.tool()
def init_objects_data() -> str:
  """
  Blender scene의 모든 오브젝트를 삭제하여 씬을 초기화합니다.
  종이접기 작업을 새로 시작하기 전에 호출하여 빈 씬을 준비합니다.
  """
  for id_data in bpy.data.objects:
        bpy.data.objects.remove(id_data)
    
  return f"init done"
        
@mcp.tool()
def create_new_plane(name='plane') -> str:
  """
  Blender scene에 정사각형 평면 메시 오브젝트를 생성합니다.
  종이접기의 시작점인 종이(평면)를 생성하는 데 사용합니다.
  Args:
      name: 생성할 오브젝트의 이름 (기본값: 'plane')
  Returns:
      생성 완료 메시지 및 오브젝트 이름 (예: "create plane done, name : plane")
  """
  bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0), scale=(1, 1, 1))

  cur_obj=bpy.context.active_object
  cur_obj.name=name

  return f"create plane done, name : {name}"

@mcp.tool()
def get_mesh_data() -> str:
  """
  현재 활성화된 오브젝트의 메시 데이터를 JSON 형식으로 반환합니다.
  종이접기 진행 상태를 확인하거나 다음 접기 작업에 사용할 꼭짓점·엣지 인덱스를 파악할 때 사용합니다.
  Returns:
      {"vertices": [[x,y,z], ...], "edges": [[v0,v1], ...], "faces": [[v0,v1,...], ...]} 형태의 JSON 문자열
  """
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
  현재 Blender 프로젝트를 output 폴더에 project.blend 파일로 저장합니다.
  Returns:
      저장된 파일의 전체 경로 문자열 (예: "Saved to: C:\\...\\output\\project.blend")
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
  """
  현재 씬의 메시 오브젝트를 FBX 형식으로 output 폴더에 내보냅니다.
  Args:
      name: 내보낼 파일 이름 (확장자 제외, 기본값: 'result')
  Returns:
      내보내기 완료 메시지 및 파일 경로 (예: "export done, path : C:\\...\\output\\result.fbx")
  """
  export_path = str(os.path.dirname(os.path.realpath(__file__))) + "\\..\\output\\" + name + ".fbx"
  bpy.ops.export_scene.fbx(filepath=export_path, object_types={'MESH'}, use_mesh_modifiers=False, add_leaf_bones=False, bake_anim=False)
  
  return f"export done, path : {export_path}"
  
@mcp.tool()
def stl_export(name='result') -> str:
  """
  현재 씬의 메시 오브젝트를 STL 형식으로 output 폴더에 내보냅니다.
  Args:
      name: 내보낼 파일 이름 (확장자 제외, 기본값: 'result')
  Returns:
      내보내기 완료 메시지 및 파일 경로 (예: "export done, path : C:\\...\\output\\result.stl")
  """
  export_path = str(os.path.dirname(os.path.realpath(__file__))) + "\\..\\output\\" + name + ".stl"
  bpy.ops.export_mesh.stl(filepath=export_path)
  
  return f"export done, path : {export_path}"