from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    config_path = os.path.join(
        get_package_share_directory("turtle_hunter_bringup"),
        "config",
        "turtle_hunter_params.yaml",
    )

    return LaunchDescription(
        [
            Node(
                package="turtlesim",
                executable="turtlesim_node",
                name="turtlesim_node",
                output="screen",
            ),
            Node(
                package="turtle_hunter",
                executable="turtle_spawner",
                name="turtle_spawner",
                parameters=[config_path],
                output="screen",
            ),
            Node(
                package="turtle_hunter",
                executable="turtle_controller",
                name="turtle_controller",
                parameters=[config_path],
                output="screen",
            ),
        ]
    )
