from urchin import URDF
import urchin
import numpy as np
import json
import os
import bpy


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

    def __init__(self, name='', origin = np.eye(4), origin_xyz = [0, 0, 0], origin_rpy = [0, 0, 0]):
        self.name = name
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


def get_info_fromURDF(input_path, output_path, ref_frame="base_link-base_link_inertia", ref_configuration= [0,0,0,0,0,-3.1415]):
    robot = URDF.load(input_path)
    filenameFront = os.path.dirname(input_path)
#########################################################
    joint_matrixs = [] #joint_matrixs 里面存储的是从urdf中依次读取到的origin matrix, 同时将ref_configuration_matrix更新到名为ref_frame上了
    linksOut = []
    for link in robot.links:
        linkToblender = Linknew()
        if link.name:
            linkToblender.name = link.name

        if link.visuals:
            filename_visual = os.path.join(filenameFront, link.visuals[0].geometry.mesh.filename)
            linkToblender.visual = filename_visual

            visual_origin = link.visuals[0].origin
            if visual_origin is not None:
                linkToblender.origin = visual_origin

                origin_xyz_rpy = urchin.matrix_to_xyz_rpy(visual_origin)
                linkToblender.origin_xyz = origin_xyz_rpy[:3].tolist()
                linkToblender.origin_rpy = origin_xyz_rpy[3:].tolist()

        if link.collisions:
            filename_collision = os.path.join(filenameFront, link.collisions[0].geometry.mesh.filename)
            linkToblender.collision = filename_collision
    
        linksOut.append(linkToblender)
        

    jointsOut = []
    for joint in robot.joints:
        jointToblender = Jointnew() #jointToblender记录的是从urdf中读取到的数据：名字，origin matrix

        if joint.name:
            jointToblender.name = joint.name
        
        if joint.origin.size:
            jointToblender.origin = joint.origin
        if joint.name == ref_frame:
            joint_matrixs.append(urchin.xyz_rpy_to_matrix(ref_configuration))
            joint.origin_xyz = ref_configuration[:3]
            joint.origin_rpy = ref_configuration[3:]
        else:
            joint_matrixs.append(joint.origin)

        jointsOut.append(jointToblender)
###############################################################################
    ref_matrix = urchin.xyz_rpy_to_matrix(ref_configuration)
    
    
    joint_position_matrices = [np.eye(4)] #joint_position_matrices 存储的是进行foward kinematic之后每个joint在世界坐标系下的位置
    for joint_matrix in joint_matrixs:
        current_joint = joint_position_matrices[-1] @ joint_matrix
        joint_position_matrices.append(current_joint)

    del joint_position_matrices[0]

    index = 0
    for joint in jointsOut:
        joint.origin = joint_position_matrices[index]
        origin_xyz_rpy = urchin.matrix_to_xyz_rpy(joint_position_matrices[index]).tolist()
        joint.origin_xyz = origin_xyz_rpy[:3]
        joint.origin_rpy = origin_xyz_rpy[3:]

        index += 1
###############################################################################
#           
    print("所有link已成功附属于对应的joint并完成机械臂构建,link信息已经输出至text.json")

########################################################################
    data = {
        "links": [link.to_dict() for link in linksOut],
        "joints": [joint.to_dict() for joint in jointsOut],
        }

    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    

#####################################################################################

    with open(output_path, "r") as f:
        data = json.load(f)

    joints = {}

    for joint in data["joints"]:
        joint_obj = bpy.data.objects.new(joint["name"], None)
        joint_obj.location = joint["origin_xyz"] 
        joint_obj.rotation_euler = joint["origin_rpy"]
        joint_obj.empty_display_size = 0.2
        joint_obj.empty_display_type = 'ARROWS'
        bpy.context.collection.objects.link(joint_obj)
        joints[joint["name"]] = joint_obj 

    for index, link in enumerate(data["links"]):
        if link["collision"]:
            bpy.ops.import_mesh.stl(filepath=link["collision"])
        else:
            continue

        visual_obj = bpy.context.selected_objects[0] 
        visual_obj.name = link["name"]

        if index == 0:
            visual_obj.location = link["origin_xyz"]
            visual_obj.rotation_euler = link["origin_rpy"]
            previous_link = visual_obj
        else:
            joint = data["joints"][index - 1]
            joint_obj = joints[joint["name"]]
            visual_obj.parent = joint_obj 

            visual_obj.location = link["origin_xyz"] 
            visual_obj.rotation_euler = link["origin_rpy"]


    '''with open(output_path, "r") as file:
        data = json.load(file)

    for i, joint in enumerate(data["joints"]):
        if i < len(joint_position_matrices):
            joint_xyz_rpy = urchin.matrix_to_xyz_rpy(joint_position_matrices[i]).tolist()


    with open(output_path, "w") as file:
        json.dump(data, file, indent=4)'''

    print("Successfully get information from URDF!")
    
def main():
    get_info_fromURDF(input_path= "/home/haitaoxu/code/robot_dart-master/utheque/ur3e/ur3e.urdf", output_path= '/home/haitaoxu/code/output_data.json')


if __name__ == "__main__":
    main()
