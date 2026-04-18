from mcp_instance import mcp
from tools.fold import *
from tools.blender_utils import *
from recipe.paper_airplane import *
from recipe.paper_crane import *

@mcp.tool()
def create_and_export_paper_crane() -> str:
  """
  종이접기를 통해 paper crane을 생성하고 export 합니다.
  """
  init_objects_data()
  create_new_plane()
  create_paper_crane()
  fbx_export("paper_crane")
  
  return f"Done"

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport="stdio")