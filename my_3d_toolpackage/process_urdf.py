from urchin import URDF
import urchin
import numpy as np
import json
import os
import bpy

# 定义库中所用到的link和joint的类，同时也是输出的类
class Linknew:
    def __init__(self, name='', visual='', collision='', origin = np.eye(4), origin_xyz = [0, 0, 0],origin_rpy = [0, 0, 0]):
        self.name = name
        self.visual = visual
        self.collision = collision
        self.origin = origin
        self.origin_xyz = origin_xyz
        self.origin_rpy = origin_rpy
        
    def to_dict(self):
        return {
            "name": self.name,
            "visual": self.visual,
            "collision": self.collision,
            #"origin": self.origin.tolist(),
            "origin_xyz": self.origin_xyz,
            "origin_rpy": self.origin_rpy,
        }

class Jointnew:
    def __init__(self, name='', parent= '', child= '',  origin = np.eye(4), origin_xyz = [0, 0, 0], origin_rpy = [0, 0, 0]):
        self.name = name
        self.parent = parent
        self.child = child
        self.origin = origin
        self.origin_xyz = origin_xyz
        self.origin_rpy = origin_rpy

    def to_dict(self):
        return {
            "name": self.name,
            #"origin": self.origin.tolist(),
            "origin_xyz": self.origin_xyz,
            "origin_rpy": self.origin_rpy,
        }

def get_linksdata(robot, filenameFront): # 在linksOut中键为每一个link的名字, 值为Linknew类 存储每一个link的名字, xyz, rpy, visual的3d模型路径, collision的3d模型路径
    linksOut = {}
    for link in robot.links:
        linkToblender = Linknew()
        if link.name:
            linkToblender.name = link.name

        if link.visuals:
            linkToblender.origin = link.visuals[0].origin

        if link.visuals and link.visuals[0].geometry and link.visuals[0].geometry.mesh and link.visuals[0].geometry.mesh.filename:
            if link.visuals[0].geometry.mesh.filename.endswith((".stl", ".glb", ".obj", ".STL", ".GLB", ".OBJ")):
                linkToblender.visual = os.path.join(filenameFront, link.visuals[0].geometry.mesh.filename)
            else:
                print(f"警告: link {link.name} visual的模型不是stl/glb/obj文件!")
        else:
            print(f"警告: link {link.name}的视觉网格缺失或无效!")

        if link.collisions and link.collisions[0].geometry and link.collisions[0].geometry.mesh and link.collisions[0].geometry.mesh.filename:
            if link.collisions[0].geometry.mesh.filename.endswith((".stl", ".glb", ".obj", ".STL", ".GLB", ".OBJ")):
                linkToblender.collision = os.path.join(filenameFront, link.collisions[0].geometry.mesh.filename)
            else:
                print(f"警告: link {link.name}的collision的模型不是stl/glb/obj文件!")
        else:
            print(f"警告: link {link.name}的碰撞网格缺失或无效!")
    
        linksOut[link.name] = linkToblender
    return linksOut

def get_jointsdata(robot): #jointOut以Jointnew类存储每一个joint的名字, origin matrix, xyz, rpy, 
    jointsOut = {}
    for joint in robot.joints:
        jointToblender = Jointnew() 
        if joint.name:
            jointToblender.name = joint.name
        if joint.parent:
            jointToblender.parent = joint.parent
        if joint.child:
            jointToblender.child = joint.child
            
        jointsOut[joint.name] = jointToblender
    return jointsOut

def FK_and_update_link_xyzrpy(robot, linksOut, jointsOut, ref_joint, ref_config): #计算正运动学并将世界坐标系下joint的xyz, rpy更新到jointsOut
    if ref_joint: #计算正运动学，得到各个link worldframe的位姿
        ref = dict(zip(ref_joint, ref_config))
        fk_result = robot.link_fk(ref) 
    else:
        fk_result = robot.link_fk()

    ChildLinkname_ParentJointmatrix = dict()
    for Link, pose in fk_result.items(): #注意： urdf中的link_fk中返回的不是官网上所说的links的位姿，而是返回的joints的位姿！！！所以必须还要将这些齐次矩阵和urdf中每个link的齐次矩阵再相乘一次
        linksOut[Link.name].origin = np.dot(pose, linksOut[Link.name].origin)
        linksOut[Link.name].origin_xyz = urchin.matrix_to_xyz_rpy(linksOut[Link.name].origin).tolist()[:3]
        linksOut[Link.name].origin_rpy = urchin.matrix_to_xyz_rpy(linksOut[Link.name].origin).tolist()[3:]
        ChildLinkname_ParentJointmatrix[Link.name] = pose
        
    for joint in jointsOut.values():
        joint.origin = ChildLinkname_ParentJointmatrix[joint.child]
        joint.origin_xyz = urchin.matrix_to_xyz_rpy(joint.origin).tolist()[:3]
        joint.origin_rpy = urchin.matrix_to_xyz_rpy(joint.origin).tolist()[3:]
        
    return linksOut, jointsOut

def show_in_blender(data): #在blender中显示出link和joint的坐标轴
    for joint in data["joints"]: # 在blender世界坐标系下搭建好每个joint并显示出坐标轴
        joint_obj = bpy.data.objects.new(joint["name"], None)
        joint_obj.location = joint["origin_xyz"] 
        joint_obj.rotation_euler = joint["origin_rpy"]
        joint_obj.empty_display_size = 0.4
        joint_obj.empty_display_type = 'ARROWS'
        bpy.context.collection.objects.link(joint_obj)

    for link in data["links"]: #在blender中将links的3d模型导出
        if link["collision"]: 
            if link["collision"].endswith((".stl", ".STL")):
                bpy.ops.import_mesh.stl(filepath=link["collision"]) 
            elif link["collision"].endswith((".glb", ".GLB")):
                bpy.ops.import_scene.gltf(filepath=link["collision"])
            elif link["collision"].endswith((".obj", ".OBJ")):
                bpy.ops.wm.obj_import(filepath=link["collision"])
        elif link["visual"]:
            print("没有导入link['collision']")
            if link["visual"].endswith((".stl", ".STL")):
                bpy.ops.import_mesh.stl(filepath=link["visual"]) 
            elif link["visual"].endswith((".glb", ".GLB")):
                bpy.ops.import_scene.gltf(filepath=link["visual"])
            elif link["visual"].endswith((".obj", ".OBJ")):
                bpy.ops.wm.obj_import(filepath=link["visual"])
        else:
            continue

        visual_obj = bpy.context.selected_objects[0] 
        visual_obj.name = link["name"]

        visual_obj.location = link["origin_xyz"] 
        visual_obj.rotation_euler = link["origin_rpy"]
            

    #print("所有link已成功附属于对应的joint并完成机械臂构建")

def joint_in_local_or_world(robot, joint_xyzrpy_in_LocalFrame, data): #如果指令中有joint_localframe, 则执行下面的代码,输出附坐标系下的joint的位姿
    if joint_xyzrpy_in_LocalFrame: 
        index = 0
        for joint in data["joints"]:
            xyzrpy = urchin.matrix_to_xyz_rpy(robot.joints[index].origin).tolist()
            joint["origin_xyz"] = xyzrpy[:3]
            joint["origin_rpy"] = xyzrpy[3:]
            index += 1


def get_info_fromURDF(input_path, output_path, ref_joint, ref_config, joint_xyzrpy_in_LocalFrame):
    robot = URDF.load(input_path)
    filenameFront = os.path.dirname(input_path)

    linksOut = get_linksdata(robot, filenameFront) #在linksOut中以Linknew类存储每一个link的名字, xyz, rpy, visual的3d模型路径, collision的3d模型路径
    jointsOut = get_jointsdata(robot) #jointOut以Jointnew类存储每一个joint的名字, origin matrix
    linksOut, jointsOut = FK_and_update_link_xyzrpy(robot, linksOut, jointsOut, ref_joint, ref_config) #计算正运动学并将世界坐标系下joint的xyz, rpy更新到jointsOut

    data = {
        "links": [link.to_dict() for link in linksOut.values()],
        "joints": [joint.to_dict() for joint in jointsOut.values()],
        }

    show_in_blender(data) #在blender中显示出link和joint的坐标轴
    joint_in_local_or_world(robot, joint_xyzrpy_in_LocalFrame, data) #如果指令中有joint_localframe, 则执行下面的代码,输出附坐标系下的joint的位姿

    with open(output_path, "w") as json_file: # 输出从urdf中读取到的links和joints的信息
        json.dump(data, json_file, indent=4)

    return data


