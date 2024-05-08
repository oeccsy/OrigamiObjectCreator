from Modules.fold import *

def create_papercrane():
  triangle_fold(2,1)
  triangle_fold(3,0)

  perpendicular_bisect(1,3)
  reverse_fold(3,[12,13])
  rotate_v_around_e(8,7)

  reverse_fold(0,[14,15])
  rotate_v_around_e(5,7)

  angle_bisect(2,4)
  angle_bisect(11,4)
  angle_bisect(9,5)
  angle_bisect(0,5)
  reverse_fold(7,[18,20])
  reverse_fold(8,[25,26])
  reverse_fold(6,[20,21])
  reverse_fold(5,[25,27])

  v1v2_axis_fold(3,v1_index=10,v2_index=12)
  v1v2_axis_fold(0,v1_index=10,v2_index=12)

  icecream_fold(25,31)
  icecream_fold(24,31)
  icecream_fold(20,30)
  icecream_fold(19,30)

  reverse_fold(1,[37,38])
  reverse_fold(2,[36,39])

  v1v2_axis_fold(3,v1_index=22,v2_index=32,angle=math.pi/3)
  v1v2_axis_fold(0,v1_index=22,v2_index=32,angle=-math.pi/3)

  bisect((0.5,0.7,0),(-1,1,0))
  rotate_v_around_e(2,196)

