import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

from my_3d_toolpackage.createConvexHull import create_convex_hull
from my_3d_toolpackage.simplify import simplify
from my_3d_toolpackage.process_urdf import get_info_fromURDF
from my_3d_toolpackage.exportInWorldframe import export_in_WorldFrame


def main():
    urdf_input_path = "/home/haitaoxu/code/robot_dart-master/utheque/ur3e/ur3e.urdf"
    output_folder = '/home/haitaoxu/Project_root/my_3d_toolpackage'
    output_path = output_folder + "/output_data.json"

    get_info_fromURDF(urdf_input_path, output_path)
    print("URDF information extracted successfully.")


    convex_hull = create_convex_hull(output_path)
    print("Convex hull created successfully.")


    simplify(output_path, decimate_ratio=0.05)
    print("Mesh simplified successfully.")


    export_in_WorldFrame(output_folder)
    print("Successfully export in World Frame")



if __name__ == "__main__":
    main()

