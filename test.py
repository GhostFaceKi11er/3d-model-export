import bpy
import os
import json
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete() # 清除blender中的所有对象

from my_3d_toolpackage.createConvexHull import create_convex_hull
from my_3d_toolpackage.simplify import simplify
from my_3d_toolpackage.process_urdf import get_info_fromURDF
from my_3d_toolpackage.exportInWorldframe import export_in_WorldFrame
import argparse


def main():
    parser = argparse.ArgumentParser(prog='test',description=(
        '''
        urdf_path='/home/haitaoxu/code/robot_dart-master/utheque/ur3e/ur3e.urdf'   输入urdf的路径
        output_foler='/home/haitaoxu/3d-model-export/data'   输入输出数据的文件夹路径
        
        --output_type 指定输出文件类型. 选项: stl、glb、obj
        --decimate=0.1   输入decimate ratio来简化模型
        --ref_joint='base_link_inertia,shoulder_link'   输入某一个或某几个joint的名字, 该joint的关节角将由用户手动输入设置
        --ref_config='1.57,1.57,'   输入需要特定设置的joint的关节角
        --create_convex_hull  输入指令创建凸包
        --joint_localframe 默认joint的xyzrpy在输出的json文件中为worldframe,如果需要的是附坐标系就输入指令'''), formatter_class=argparse.RawDescriptionHelpFormatter)

    def check_decimate_ratio(value):
        try:
            fvalue = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid value: {value}. 务必是0到1之间的小数")
        
        if 0 <= fvalue <= 1:
            return fvalue
        else:
            raise argparse.ArgumentTypeError(f"Invalid value: {value}. 务必在0到1之间")

    def parse_comma_separated_floats(value):
        try:
            return [float(x) for x in value.split(',')]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid configuration: {value}, 务必按正确格式输入！")

    def parse_comma_separated_strings(value):
        try:
            return [x for x in value.split(',')]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid configuration: {value}, 务必按正确格式输入！")

    parser.add_argument('urdf_path', help="输入urdf的路径 示例: --urdf_path='/home/haitaoxu/code/robot_dart-master/utheque/ur3e/ur3e.urdf'")
    parser.add_argument('output_folder', help="输入输出数据的文件夹路径. 该文件夹中有blend文件, 每个link的stl文件, 以及存储每个link和joint的名字, xyz,rpy,visaul的文件路径, 简化后的collision的文件路径示例: --output_foler='/home/haitaoxu/3d-model-export/data'")
    
    parser.add_argument('--output_type', choices=['stl', 'glb', 'obj'], default='stl', help="指定link的输出文件类型. 选项: stl、glb、obj 默认为 stl. 示例: --output_type glb")
    parser.add_argument('--decimate_ratio', type=check_decimate_ratio, help="输入decimate ratio来简化模型, 范围为(0, 1) 默认为1, 即不简化 示例: --decimate=0.1",default=1)
    parser.add_argument('--ref_joint', type=parse_comma_separated_strings, help="输入某一个或某几个joint的名字, 该joint的关节角将由用户手动输入设置 示例: --ref_joint='shoulder_pan_joint,elbow_joint'")
    parser.add_argument('--ref_config', type=parse_comma_separated_floats, help="输入需要特定设置的joint的关节角 示例: --ref_config='1.57,1.57'")
    parser.add_argument('--create_convex_hull', action='store_true', help="启用凸包创建功能（默认禁用）")
    parser.add_argument('--joint_localframe', action='store_true', help="joint启用附坐标系, 默认joint的xyzrpy在输出的json文件中为worldframe")
    
    args = parser.parse_args()

    output_path = args.output_folder + "/output_data.json" # 输出数据的完整路径
    urdf_input_path = args.urdf_path # 输入的urdf文件的路径
    directory_path = args.output_folder #如果文件夹不存在就新建一个
    os.makedirs(directory_path, exist_ok=True)
    output_folder = args.output_folder #设置部分变量名
    decimate_ratio = args.decimate_ratio 
    ref_joint = args.ref_joint
    ref_config = args.ref_config
    joint_xyzrpy_in_LocalFrame = args.joint_localframe
    output_type = args.output_type


    data = get_info_fromURDF(urdf_input_path, output_path, ref_joint, ref_config, joint_xyzrpy_in_LocalFrame) # 从urdf中获取数据并处理，将需要的数据导出到output_path中
    print("URDF information extracted successfully.\n")


    if args.create_convex_hull:
        create_convex_hull(data) # 对每个模型建立凸包
        print("Convex hull created successfully.\n")

    if decimate_ratio != 1:
        simplify(decimate_ratio, data) # 对每个3d模型进行简化
        print("Mesh simplified successfully.\n")


    export_in_WorldFrame(output_type, output_folder, output_path, data) # 将处理后的3d模型和blend文件导出，并在数据json文件中更新路径
    print("Successfully export in World Frame\n")



if __name__ == "__main__":
    main()

