import bpy
#import math
#import random

#store selection
obs = bpy.context.selected_objects

### remove for templates of correct scales
bpy.ops.transform.resize(
    value=(3550, 3550, 3550),
    orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
    mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
### /remove for templates of correct scales

# Get material
backmat = bpy.data.materials.get("BackMat.001")
if backmat is None:
    # create material
    backmat = bpy.data.materials.new(name="BackMat.001")

frontmat = bpy.data.materials.get("FrontMat.001")
if frontmat is None:
    # create material
    frontmat = bpy.data.materials.new(name="FrontMat.001")


for ob in obs:
    #deselect all but just one object and make it active
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob
    
    bpy.context.object.data.resolution_u = 3
    bpy.ops.object.convert(target='MESH', keep_original= False)

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.dissolve_limited()
    bpy.ops.mesh.mark_sharp(use_verts=True)
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = 0.075
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")

    bpy.ops.object.modifier_add(type='EDGE_SPLIT')
    bpy.context.object.modifiers["EdgeSplit"].split_angle = 1.05069 # 60 degrees
    #bpy.context.object.modifiers["EdgeSplit"].use_edge_angle = False
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="EdgeSplit")
    

    bpy.ops.object.shade_flat()
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    
    ob.data.polygons[1].select = True
    
    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.mesh.select_linked()
    #bpy.ops.object.material_slot_add()
    ob.data.materials[0] = frontmat
    bpy.context.object.active_material_index = 0
    bpy.ops.object.material_slot_assign()

    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.object.material_slot_add()
    ob.data.materials[1] = backmat
    bpy.context.object.active_material_index = 1
    bpy.ops.object.material_slot_assign()

    bpy.ops.object.material_slot_move(direction='UP')
    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)



#reselect originally selected objects  
for ob in obs:
    ob.select_set(state=True)


bcat = bpy.context.area.type
bpy.context.area.type = 'VIEW_3D'
bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
bpy.context.area.type = bcat