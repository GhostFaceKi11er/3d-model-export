import bpy
import json
import os

def update_json_with_collision_paths(joint_xyzrpy_in_LocalFrame, collection, output_type, output_folder, output_path, data):
    scale = 0
    for link in data["links"]:
        if link['collision'] or link['visual']:
            link_name = link["name"]
            bpy.ops.object.select_all(action='DESELECT')
            obj = bpy.data.objects.get(link_name)
            if obj:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                #obj.rotation_mode = 'XYZ'
                if joint_xyzrpy_in_LocalFrame:
                    temp_location = obj.location.copy()
                    temp_rotation = obj.rotation_euler.copy()
                    obj.location = [0, 0, 0]
                    obj.rotation_euler = [0, 0, 0]
                if output_type == 'glb': #选择输出为glb文件
                    export_path = f"{output_folder}/{link_name}.glb"
                    bpy.ops.export_scene.gltf(filepath=export_path, use_selection=True, export_format="GLB")
                elif output_type == 'obj': #选择输出为obj文件
                    export_path = f"{output_folder}/{link_name}.obj"
                    bpy.ops.wm.obj_export(filepath=export_path, export_selected_objects=True, forward_axis='Y', up_axis='Z')
                else: #默认输出为stl文件
                    export_path = f"{output_folder}/{link_name}.stl"
                    bpy.ops.export_mesh.stl(filepath=export_path, use_selection=True, axis_forward='Y', axis_up='Z')
                link["collision"] = export_path

                if joint_xyzrpy_in_LocalFrame:
                    obj.location = temp_location
                    obj.rotation_euler = temp_rotation
                
                for i in obj.location: #得到整个机器人x,y,z最大的绝对位置
                    scale = max(abs(i), scale)

                bpy.ops.object.select_all(action='DESELECT')
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    return scale, data
                
def export_in_WorldFrame(joint_xyzrpy_in_LocalFrame, output_type, output_folder, output_path, data, image):
    target_collection = bpy.data.collections['Collection']
    scale, data = update_json_with_collision_paths(joint_xyzrpy_in_LocalFrame, target_collection, output_type, output_folder, output_path, data)

    blend_output_path = output_folder + "/output_blend.blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_output_path)

    if image:
        bpy.context.scene.render.filepath = output_folder + "/image.png"  # 请将此路径修改为你想保存图片的位置

        bpy.context.scene.render.resolution_x = 640  # 宽度 #设置渲染的分辨率
        bpy.context.scene.render.resolution_y = 360  # 高度

        camera_loc = [0, -scale*15, scale*9]
        if bpy.context.scene.camera is None: # 如果没有相机，则添加一个新的相机
            bpy.ops.object.camera_add(location=camera_loc)

            camera = bpy.context.object
            camera.rotation_euler = (1.1, 0, 0)  # 设置相机的旋转角度
            bpy.context.scene.camera = camera  # 将相机设置为当前活动相机
        bpy.ops.object.light_add(type='POINT', location=camera_loc)
        light = bpy.context.object
        light.data.energy = 1000  # 增加光源强度

        bpy.ops.render.render(write_still=True)



