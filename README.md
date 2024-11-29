# MeshMan
基于blender(3.6.0)的机器人外发模型操作工具

# 终端指令
usage: test [-h] [--output_type {stl,glb,obj}] [--decimate_ratio DECIMATE_RATIO] [--ref_joint REF_JOINT] [--ref_config REF_CONFIG] [--create_convex_hull] [--joint_localframe]
            urdf_path output_folder

        urdf_path='./ur3e/ur3e.urdf'   输入urdf的路径
        output_foler='./data'   输入输出数据的文件夹路径
        
        --output_type 指定输出文件类型. 选项: stl、glb、obj
        --decimate=0.1   输入decimate ratio来简化模型
        --ref_joint='base_link_inertia,shoulder_link'   输入某一个或某几个joint的名字, 该joint的关节角将由用户手动输入设置
        --ref_config='1.57,1.57,'   输入需要特定设置的joint的关节角
        --create_convex_hull  输入指令创建凸包
        --joint_localframe 默认joint的xyzrpy在输出的json文件中为worldframe,如果需要的是附坐标系就输入指令

positional arguments:
  urdf_path             输入urdf的路径 示例: --urdf_path='./ur3e/ur3e.urdf'
  output_folder         输入输出数据的文件夹路径. 该文件夹中有blend文件, 每个link的stl文件, 以及存储每个link和joint的名字, xyz,rpy,visaul的文件路径, 简化后的collision的文件路径示例: --output_foler='./data'

options:
  -h, --help            show this help message and exit
  --output_type {stl,glb,obj}
                        指定link的输出文件类型. 选项: stl、glb、obj 默认为 stl. 示例: --output_type glb
  --decimate_ratio DECIMATE_RATIO
                        输入decimate ratio来简化模型, 范围为(0, 1) 默认为1, 即不简化 示例: --decimate=0.1
  --ref_joint REF_JOINT
                        输入某一个或某几个joint的名字, 该joint的关节角将由用户手动输入设置 示例: --ref_joint='shoulder_pan_joint,elbow_joint'
  --ref_config REF_CONFIG
                        输入需要特定设置的joint的关节角 示例: --ref_config='1.57,1.57'
  --create_convex_hull  启用凸包创建功能（默认禁用）
  --joint_localframe    joint启用附坐标系, 默认joint的xyzrpy在输出的json文件中为worldframe

# 代码框架


# 功能
从urdf中读取模型信息
- 简化
- 在特定姿态下更改参考坐标系为基座坐标系
- 建convex_hull

# 示例
```
python test.py './iiwa/iiwa.urdf' './data' --decimate=0.5 --create_convex_hull --ref_joint='iiwa_joint_5,iiwa_joint_6' --ref_config='1.57,1.57'

python test.py './ur3e/ur3e.urdf' './data' --decimate=0.5 --create_convex_hull --output_type glb --ref_joint='shoulder_pan_joint,elbow_joint' --ref_config='1.57,1.57'

python test.py './franka/franka.urdf' './data' --decimate=0.5 --create_convex_hull --ref_frame='local' --ref_joint='panda_joint2,panda_joint4'  --ref_config='1.57,1.57'

```
