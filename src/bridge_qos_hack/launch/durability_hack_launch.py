from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution

from launch_ros.actions import Node

def generate_launch_description():

    real_pub = DeclareLaunchArgument(
      'real_pub', default_value=TextSubstitution(text='map')
    )
    
    fake_pub = DeclareLaunchArgument(
      'fake_pub', default_value=TextSubstitution(text='nav2_map')
    )
    
    return LaunchDescription([
        real_pub,
        fake_pub,
        Node(
            package = 'bridge_qos_hack',
            executable = 'map_hack',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'real_pub': LaunchConfiguration('real_pub'),
                'fake_pub': LaunchConfiguration('fake_pub'),
            }]
        )
    ])
