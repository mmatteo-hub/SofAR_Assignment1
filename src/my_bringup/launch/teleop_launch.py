from launch import LaunchDescription

from launch_ros.actions import Node

def generate_launch_description():

    #Creating a teleop Node with remapped topic
    teleop_node = Node(
        package = 'teleop_twist_keyboard',
        executable = 'teleop_twist_keyboard',
        output='screen',
        emulate_tty=True,
        remappings=[
            ('/cmd_vel', '/mobile_base_controller/cmd_vel')
        ]
    )
    
    return LaunchDescription([
        teleop_node,
    ])