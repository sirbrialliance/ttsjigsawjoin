import bpy

#store selection
obs = bpy.context.selected_objects

bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

for ob in obs:
    for poly in ob.data.polygons:
        if poly.material_index == 1:
            poly.select = True

bpy.ops.object.mode_set(mode='EDIT', toggle=False)
