import bpy
import json

def simplify(output_path, decimate_ratio):
    with open(output_path, 'r') as f:
            data = json.load(f)

    for link_info in data["links"]:
        if link_info['collision'] != '':
            link_name = link_info["name"]
            bpy.ops.object.select_all(action='DESELECT')
            obj = bpy.data.objects.get(link_name)
                
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type="DECIMATE")
            bpy.data.objects[link_name].modifiers["Decimate"].ratio = decimate_ratio


