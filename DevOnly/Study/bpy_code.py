import bpy

def check_editor_use():
  try:
    bpy.context
    return True
  except NameError:
    return False