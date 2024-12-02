import bpy
import json

def create_convex_hull(data):
    for link in data["links"]:
        if link['collision'] or link['visual']:
            link_name = link["name"]
            bpy.ops.object.select_all(action='DESELECT')
            obj = bpy.data.objects.get(link_name)
                    
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.convex_hull()
            bpy.ops.object.mode_set(mode='OBJECT')