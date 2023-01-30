import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

# this is the function launch  system will look for
def generate_launch_description():

    ####### DATA INPUT ##########
    urdf_file = 'ai_rover.urdf'
    # xacro_file = "box_bot.xacro"
    rviz_file = 'ai_rover_urdf_vis.rviz'
    package_description = "ai_rover_description"
    root_p = get_package_share_directory(package_description)

    ####### DATA INPUT END ##########
    print("Fetching URDF ==>")
    robot_desc_path = os.path.join(root_p, "urdf", urdf_file)

    robot_description = ParameterValue(Command(['xacro ', robot_desc_path]), value_type=str)
    # Robot State Publisher

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        emulate_tty=True,
        parameters=[{'use_sim_time': True, 'robot_description': robot_description}],
        output="screen"
    )

    # RVIZ Configuration
    rviz_config_dir = os.path.join(root_p, 'rviz', rviz_file)
    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            output='screen',
            name='rviz_node',
            parameters=[{'use_sim_time': True}],
            arguments=['-d', rviz_config_dir])

    # create and return launch description object
    return LaunchDescription(
        [            
            robot_state_publisher_node,
            rviz_node
        ]
    )