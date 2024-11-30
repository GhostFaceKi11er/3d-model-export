import bpy
import json

def simplify(decimate_ratio, data):
    for link in data["links"]:
        if link['collision'] or link['visual']:
            link_name = link["name"]
            bpy.ops.object.select_all(action='DESELECT')
            obj = bpy.data.objects.get(link_name)
                
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type="DECIMATE")
            bpy.data.objects[link_name].modifiers["Decimate"].ratio = decimate_ratio


