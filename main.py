from mcp_instance import mcp
from tools.fold import *
from tools.blender_utils import *
from recipe.paper_airplane import *
from recipe.paper_crane import *

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport="stdio")