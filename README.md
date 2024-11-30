# model_export
基于blender(3.6.0)的机器人外发模型操作工具

# 基本信息
'''
setup(
    name='model_export',  
    version='0.1.0',  
    description='A toolpackage for 3D processing and manipulation in Python from urdf to blender',   
    author='Haitao Xu',    
    author_email='haitaoxu_tok@outlook.com',   
    url='https://github.com/GhostFaceKi11er/3d-model-export.git',  
    install_requires=[  
        'bpy: 3.6.0',  
        'urchin: 0.0.29(默认的最新版)',  
        'numpy: 2.1.3(默认的最新版)/1.23.5',  
        'networkx: 3.4.2(默认的最新版)/2.2',  
        'PyYAML: 5.4.1'  
    ],  
    注意: 如果电脑一开始没有numpy和networkx, 那么直接安装urchin就会自动安装这两个库. pip install urchin  
    python=3.10.12,  
)  
'''
 #  帮助
'''
usage: test [-h] [--output_type {stl,glb,obj}] [--decimate_ratio DECIMATE_RATIO] [--create_convex_hull] [--joint_localframe] urdf_path output_folder yaml_path  

positional arguments:  
  urdf_path             输入urdf的路径 示例: './ur3e/ur3e.urdf'  
  output_folder         输入输出数据的文件夹路径. 该文件夹中有blend文件, 每个link的stl文件, 以及存储每个link和joint的名字, xyz,rpy,visaul的文件路径, 简化后的collision的文件路径示例: --output_foler='./data'  
  yaml_path             输入yml的路径, 存储的是joints的configuration 示例: './models/franka/franka_joints.yaml'  

options:  
  -h, --help            show this help message and exit  
  --output_type {stl,glb,obj}  
                        指定link的输出文件类型. 选项: stl、glb、obj 默认为 stl. 示例: --output_type glb  
  --decimate_ratio DECIMATE_RATIO  
                        输入decimate ratio来简化模型, 范围为(0, 1) 默认为1, 即不简化 示例: --decimate=0.1  
  --create_convex_hull  启用凸包创建功能（默认禁用）  
  --joint_localframe    joint启用附坐标系, 默认joint在输出的模型文件和json文件中为worldframe  
'''
# 代码框架


# 功能
从urdf中读取模型信息
- 简化
- 建convex_hull
- 在特定姿态下更改参考坐标系为基座坐标系
- 导出3d模型

# 示例
```
python -m <exectue-file> <urdf-path> <output-folder> <yaml-path> <--decimate=decimate_ratio> <--create_convex_hull> <--joint_localframe>


python -m script.main './models/iiwa/iiwa.urdf' './data' './models/iiwa/iiwa_joints.yaml' --decimate=0.5 --create_convex_hull

python -m script.main './models/ur3e/ur3e.urdf' './data' './models/ur3e/ur3e_joints.yaml' --decimate=0.5 --create_convex_hull

python -m script.main './models/franka/franka.urdf' './data' './models/franka/franka_joints.yaml' --decimate=0.5 --create_convex_hull

```

