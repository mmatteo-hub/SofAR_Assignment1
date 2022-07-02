from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
   return LaunchDescription([
    Node(
        package = 'policy_controller',
        executable = 'policy_controller',
        output = "screen",
    )
])