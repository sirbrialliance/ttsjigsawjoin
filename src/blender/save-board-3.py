import bpy
import math
import mathutils
import random

#example path to store files
path = bpy.path.abspath('//')

#store selection
obs = bpy.context.selected_objects

for ob in obs:
    #deselect all but just one object and make it active
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob

    # export obj
    filename = path + 'board.obj'
    bpy.ops.export_scene.obj(filepath=filename, use_selection=True)
