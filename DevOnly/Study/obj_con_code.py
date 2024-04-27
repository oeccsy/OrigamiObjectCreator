import bpy

### obj 선택

def select_obj(name="NewObj"):
  bpy.data.objects[name].select_set(True)
  
# active_object는 단일 오브젝트를 나타내고,
# selected_objects는 여러 오브젝트의 목록을 나타낸다.

# 만약 사용자가 하나의 오브젝트만 선택한 경우
# active_object 와 selected_objects 는 동일한 오브젝트를 나타낸다.

# 여러 오브젝트가 선택된 경우
# active_object는 마지막으로 선택된 오브젝트를 나타내고,
# selected_objects는 모든 선택된 오브젝트의 목록을 나타낸다.
  
def get_active_obj():
  return bpy.context.active_object

def get_selected_objs():
  return bpy.context.selected_objects
