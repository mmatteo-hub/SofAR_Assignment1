from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution

from launch_ros.actions import Node

def generate_launch_description():

    # The two positions as arguments for the nodes
    r1_initial_pose_argument = DeclareLaunchArgument(
      'r1_initial_pose', default_value=TextSubstitution(text="[-2.0, -5.0, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    r1_goal_pose_argument = DeclareLaunchArgument(
      'r1_goal_pose', default_value=TextSubstitution(text="[-3.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    r2_initial_pose_argument = DeclareLaunchArgument(
      'r2_initial_pose', default_value=TextSubstitution(text="[-5.0, -2.0, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    r2_goal_pose_argument = DeclareLaunchArgument(
      'r2_goal_pose', default_value=TextSubstitution(text="[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    
    r1_controller = Node(
            package = 'robot_controller',
            executable = 'robot_controller',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'robot_name': 'tiago1'},
                {
                    'initial_pose': LaunchConfiguration('r1_initial_pose'),
                    'goal_pose': LaunchConfiguration('r1_goal_pose')
                }
            ],
            remappings=[
                ('/bt_navigator/get_state', '/tiago1/bt_navigator/get_state'),
                ('/amcl/get_state', '/tiago1/amcl/get_state'),
                ('/amcl_pose', '/tiago1/amcl_pose'),
                ('/initialpose', '/tiago1/initialpose'),
                ('/map_server/load_map', '/tiago1/map_server/load_map'),
                ('/global_costmap/clear_entirely_global_costmap', '/tiago1/global_costmap/clear_entirely_global_costmap'),
                ('/local_costmap/clear_entirely_local_costmap', '/tiago1/local_costmap/clear_entirely_local_costmap'),
                ('/global_costmap/get_costmap', '/tiago1/global_costmap/get_costmap'),
                ('/local_costmap/get_costmap', '/tiago1/local_costmap/get_costmap'),
                ('/reached_goal', '/tiago1/reached_goal'),
                ('/toggle_wait', '/tiago1/toggle_wait'),
                ('/global_path', '/tiago1/global_path'),
                ('/other_reached_goal', '/tiago2/reached_goal')
            ]
        )
        
    r2_controller = Node(
        package = 'robot_controller',
        executable = 'robot_controller',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'robot_name': 'tiago2'},
            {
                'initial_pose': LaunchConfiguration('r2_initial_pose'),
                'goal_pose': LaunchConfiguration('r2_goal_pose')
            }
        ],
        remappings=[
            ('/bt_navigator/get_state', '/tiago2/bt_navigator/get_state'),
            ('/amcl/get_state', '/tiago2/amcl/get_state'),
            ('/amcl_pose', '/tiago2/amcl_pose'),
            ('/initialpose', '/tiago2/initialpose'),
            ('/map_server/load_map', '/tiago2/map_server/load_map'),
            ('/global_costmap/clear_entirely_global_costmap', '/tiago2/global_costmap/clear_entirely_global_costmap'),
            ('/local_costmap/clear_entirely_local_costmap', '/tiago2/local_costmap/clear_entirely_local_costmap'),
            ('/global_costmap/get_costmap', '/tiago2/global_costmap/get_costmap'),
            ('/local_costmap/get_costmap', '/tiago2/local_costmap/get_costmap'),
            ('/reached_goal', '/tiago2/reached_goal'),
            ('/toggle_wait', '/tiago2/toggle_wait'),
            ('/global_path', '/tiago2/global_path'),
            ('/other_reached_goal', '/tiago1/reached_goal')
        ]
    )
    
    return LaunchDescription([
        r1_initial_pose_argument,
        r1_goal_pose_argument,
        r1_controller,
        r2_initial_pose_argument,
        r2_goal_pose_argument,
        r2_controller
    ])
