from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
   return LaunchDescription([
    Node(
        package = 'robot_ui',
        executable = 'robot_ui',
        output = "screen",
    )
])