import bpy
import math
import mathutils
import random

#example path to store files
path = bpy.path.abspath('//')

#store selection
obs = bpy.context.selected_objects

piece = 0

solutionData = []

for ob in obs:
    #deselect all but just one object and make it active
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(state=True)
    bpy.context.view_layer.objects.active = ob

    # zero out object location so pivot point works as expected down stream
    location = ob.location.copy()
    bpy.ops.object.location_clear()

    
    # alter mesh geometry with randomized rotation to combat TTS auto alignment issues
    # snap to 90 degree increments for maximum compatability with player adjustable settings
    rotationZ = random.choice([0, 90, 180, 270])
    bpy.ops.transform.rotate(value=math.radians(rotationZ), orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    #rotation = ob.rotation_euler.copy()
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    # we intentionally translate blender's y to Unity's z
    solutionData.append({'solutionPosition':{'x':location.x,'y':1,'z':location.y},'solutionRotation':{'x':0,'y':rotationZ,'z':0}})

    # export obj
    piece += 1
    filename = path + 'piece.' + str(piece) + '.obj'
    bpy.ops.export_scene.obj(filepath=filename, use_selection=True)

    # restore location
    ob.location = location

#reselect originally selected objects  
#for ob in obs:
   # ob.select_set(state=True)




#print(solutionData)

for piece in solutionData:
    piecePos = mathutils.Vector((piece['solutionPosition']['x'], piece['solutionPosition']['y'], piece['solutionPosition']['z']))
    neighbors = []
    for candidateId, candidate in enumerate(solutionData, start=1):
        candiPos = mathutils.Vector((candidate['solutionPosition']['x'], candidate['solutionPosition']['y'], candidate['solutionPosition']['z']))
        
        deltaPos = piecePos - candiPos
        if deltaPos.length > 0 and deltaPos.length < 1.5:
            neighbors.append(str(candidateId))
        
    random.shuffle(neighbors)
        
    print('{solutionPosition={x=%f,y=1,z=%f},solutionRotation={x=0,y=%d,z=0},neighbors={%s}},' %
        (piece['solutionPosition']['x'], piece['solutionPosition']['z'], piece['solutionRotation']['y'], ','.join(neighbors)))
    
    
#print('\n'.join(solutionData))