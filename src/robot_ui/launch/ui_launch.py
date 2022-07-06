from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution

from launch_ros.actions import Node


def generate_launch_description():

    # The poses of intersest of the two robots
    # The first three elements are the positions (x, y, z)
    # The last found elements are the quaternion rotation (x, y, z, w)
    poses = [
        [-5.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        [5.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    ]
    
    # The two positions as arguments for the nodes
    pose0_argument = DeclareLaunchArgument(
      'pose0', default_value=TextSubstitution(text=str(poses[0]))
    )
    pose1_argument = DeclareLaunchArgument(
      'pose1', default_value=TextSubstitution(text=str(poses[1])
    )
    
    robot1_controller = Node(
            package = 'robot_ui',
            executable = 'robot_ui',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'robot_name': 'robot_1'},
                {
                    'initial_pose': LaunchConfiguration('pose0'),
                    'goal_pose': LaunchConfiguration('pose1')
                }],
            remappings=[
                ('/reached_goal', '/robot1/reached_goal'),
                ('/other_reached_goal', '/robot2/reached_goal'),
                ('/odom', '/robot1/odom'),
                ('/follow_path', '/robot1/follow_path'),
                ('/compute_path_to_pose', '/robot1/compute_path_to_pose'),
                ('/initialpose', '/robot1/initialpose')
                
            ]
        )
        
    robot2_controller = Node(
            package = 'robot_ui',
            executable = 'robot_ui',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'robot_name': 'robot_2'},
                {
                    'initial_pose': LaunchConfiguration('pose0'),
                    'goal_pose': LaunchConfiguration('pose1')
                }],
            remappings=[
                ('/reached_goal', '/robot2/reached_goal'),
                ('/other_reached_goal', '/robot1/reached_goal'),
                ('/odom', '/robot2/odom'),
                ('/follow_path', '/robot2/follow_path'),
                ('/compute_path_to_pose', '/robot2/compute_path_to_pose'),
                ('/initialpose', '/robot2/initialpose')
                
            ]
        )
    
    return LaunchDescription([
        pose0_argument,
        pose1_argument,
        robot1_controller,
        robot2_controller,
    ])
