import math
from mathutils import Vector
import numpy as np

### 선분p1p2를 a:b로 내분 ###
def internal_division(p1, p2, a, b):
  vector_p1p2 = p2-p1
  k = a / (a+b)

  return p1 + vector_p1p2 * k
  
