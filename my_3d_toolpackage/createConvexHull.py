import bpy
import json

def create_convex_hull(output_path):
    with open(output_path, 'r') as f:
        data = json.load(f)

    for link_info in data["links"]:
        if link_info['collision'] != '':
            link_name = link_info["name"]
            bpy.ops.object.select_all(action='DESELECT')
            obj = bpy.data.objects.get(link_name)
                    
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.convex_hull()
            bpy.ops.object.mode_set(mode='OBJECT')