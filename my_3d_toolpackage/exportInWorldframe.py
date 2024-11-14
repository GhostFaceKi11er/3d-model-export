import bpy
import json
import os

def update_json_with_collision_paths(output_path, output_folder, collection):
    with open(output_path, 'r') as f:
        data = json.load(f)

    for link_info in data["links"]:
        if link_info['collision'] != '':
            link_name = link_info["name"]
            export_path = f"{output_folder}/{link_name}.stl"
            obj = bpy.data.objects.get(link_name)
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.export_mesh.stl(filepath=export_path, use_selection=True)
            link_info["collision"] = export_path

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

def export_in_WorldFrame(output_folder):
    target_collection = bpy.data.collections['Collection']
    output_path = output_folder + "/output_data.json"

    update_json_with_collision_paths(output_path, output_folder, target_collection)





