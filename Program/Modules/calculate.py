import math
from mathutils import Vector
import numpy as np
import sympy as sp

### 선분p1p2를 a:b로 내분 ###
def internal_division(p1, p2, a, b):
  vector_p1p2 = p2-p1
  k = a / (a+b)

  return p1 + vector_p1p2 * k


### 직선의 자취 ###
def find_locus(p1, p2):
  u=(p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]) #방향 벡터
  t=sp.Symbol('t')
  result = (u[0]*t+p1[0], u[1]*t+p1[1], u[2]*t+p1[2])

  return result


### 점에서 직선에 내린 수선의 발 ###
def find_point_H(point, line):
  t=sp.Symbol('t')

  u=tuple(i.subs({t: 0}) - i.subs({t: 1}) for i in line) # 직선의 방향벡터
  n=tuple(p-l for p, l in zip(point, line)) # 수선의 발 벡터

  #dot_product=sum([uv*nv for uv, nv in zip(u, n)])
  dot_product=u[0]*n[0] + u[1]*n[1] + u[2]*n[2]
  
  value = sp.solveset(dot_product, t) #해를 찾는다.
  
  value0=float(value.args[0]) #value는 sympy의 FiniteSet

  result=tuple(i.subs({t: value0}) for i in line) # line(tuple)에 t=value0 대입

  return result