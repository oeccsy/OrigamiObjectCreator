import bpy
import bmesh

# 활성 객체의 데이터에 대한 BMesh 생성
obj = bpy.context.active_object
bm = bmesh.new()
bm.from_mesh(obj.data)

# 정점에 접근
for vert in bm.verts:
    print(vert.co)

# 엣지에 접근
for edge in bm.edges:
    print(edge.verts)

# 면에 접근
for face in bm.faces:
    print(face.normal)

# 새로운 정점 추가
v1 = bm.verts.new((0.0, 0.0, 0.0))
v2 = bm.verts.new((1.0, 0.0, 0.0))

# 새로운 엣지 추가
e = bm.edges.new((v1, v2))

# 새로운 면 추가
f = bm.faces.new((v1, v2, v3))

# 정점 이동
v1.co += mathutils.Vector((0.0, 1.0, 0.0))

# BMesh를 Blender 메시로 적용
bm.to_mesh(obj.data)
bm.free()
