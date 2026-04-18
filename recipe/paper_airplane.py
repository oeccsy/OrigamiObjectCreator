from mcp_instance import mcp
from tools.fold import *

@mcp.tool()
def create_paper_airplane() -> str:
  """
  종이접기 기법을 사용하여 현재 활성 오브젝트(평면 메시)를 종이비행기(paper airplane) 형태로 변형합니다.
  init_objects_data()와 create_new_plane()으로 씬을 준비한 후 호출해야 합니다.
  """
  parallel_bisect(1,3)
  icecream_fold(4,6)
  icecream_fold(0,6)

  e_axis_fold(4,9)

  triangle_fold(6,5)
  triangle_fold(7,5)

  icecream_fold(17,11)
  icecream_fold(20,11)
  rotate_v_around_e(9,27)
  rotate_v_around_e(10,36)

  rotate_v_around_e(12,11,-math.pi * 80 / 180)
  rotate_v_around_e(16,11,math.pi * 80 / 180)
  rotate_v_around_e(14,11,-math.pi * 80 / 180)
  rotate_v_around_e(18,11,math.pi * 80 / 180)
  rotate_v_around_e(13,11,-math.pi * 80 / 180)
  rotate_v_around_e(17,11,math.pi * 80 / 180)
  rotate_v_around_e(11,11,-math.pi * 80 / 180)
  rotate_v_around_e(15,11,math.pi * 80 / 180)

  rotate_v_around_e(3,31,math.pi/2)
  rotate_v_around_e(1,39,math.pi/2)
  
  return f"create paper crane done"

  