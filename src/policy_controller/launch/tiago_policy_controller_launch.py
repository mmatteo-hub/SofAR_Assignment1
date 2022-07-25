from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution

from launch_ros.actions import Node

def generate_launch_description():

    # Defining the robots names which are ordered by priority
    # The first robot has the maximum priority
    robot_names = DeclareLaunchArgument(
      'robot_names', default_value=TextSubstitution(text='[tiago1, tiago2]')
    )
    
    return LaunchDescription([
        robot_names,
        Node(
            package = 'policy_controller',
            executable = 'policy_controller',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'robot_names': LaunchConfiguration('robot_names'),
            }],
            remappings=[
                ('/tiago1/odom', '/tiago1/ground_truth_odom'),
                ('/tiago2/odom', '/tiago2/ground_truth_odom')
            ]
        )
    ])
