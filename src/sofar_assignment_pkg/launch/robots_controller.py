from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sofar_assignment_pkg',
            namespace='rbt1',
            executable='collision_avoidance',
            name='rbt1_controller',
            parameters=[
                {"robot_name":"RBT_1"},
            ]
        ),
        Node(
            package='sofar_assignment_pkg',
            namespace='rbt2',
            executable='collision_avoidance',
            name='rbt2_controller',
            parameters=[
                {"robot_name":"RBT_2"},
            ]
        )
    ])