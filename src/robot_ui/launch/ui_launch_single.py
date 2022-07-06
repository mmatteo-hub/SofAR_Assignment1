from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution

from launch_ros.actions import Node

def remap_action(action_name, remapped_name):
    return [
        (action_name+'/_action/cancel_goal', remapped_name+'/_action/cancel_goal'),
        (action_name+'/_action/get_result', remapped_name+'/_action/get_result'),
        (action_name+'/_action/send_goal', remapped_name+'/_action/send_goal'),
    ]

def generate_launch_description():

    # The two positions as arguments for the nodes
    r1_initial_pose_argument = DeclareLaunchArgument(
      'r1_initial_pose', default_value=TextSubstitution(text="[-4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    r1_goal_pose_argument = DeclareLaunchArgument(
      'r1_goal_pose', default_value=TextSubstitution(text="[1.0, -3.0, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    r2_initial_pose_argument = DeclareLaunchArgument(
      'r2_initial_pose', default_value=TextSubstitution(text="[-1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    r2_goal_pose_argument = DeclareLaunchArgument(
      'r2_goal_pose', default_value=TextSubstitution(text="[-1.5, -3.5, 0.0, 0.0, 0.0, 0.0, 1.0]")
    )
    
    remaps_r1 = [
        ('/bt_navigator/get_state', '/robot1/bt_navigator/get_state'),
        ('/amcl/get_state', '/robot1/amcl/get_state'),
        ('/amcl_pose', '/robot1/amcl_pose'),
        ('/initialpose', '/robot1/initialpose'),
        ('/map_server/load_map', '/robot1/map_server/load_map'),
        ('/global_costmap/clear_entirely_global_costmap', '/robot1/global_costmap/clear_entirely_global_costmap'),
        ('/local_costmap/clear_entirely_local_costmap', '/robot1/local_costmap/clear_entirely_local_costmap'),
        ('/global_costmap/get_costmap', '/robot1/global_costmap/get_costmap'),
        ('/local_costmap/get_costmap', '/robot1/local_costmap/get_costmap'),
        ('/reached_goal', '/robot1/reached_goal'),
        ('/toggle_wait', '/robot1/toggle_wait'),
        ('/global_path', '/robot1/global_path'),
        ('/other_reached_goal', '/robot2/reached_goal')
    ]
    
    remaps_r2 = [
        ('/bt_navigator/get_state', '/robot2/bt_navigator/get_state'),
        ('/amcl/get_state', '/robot2/amcl/get_state'),
        ('/amcl_pose', '/robot2/amcl_pose'),
        ('/initialpose', '/robot2/initialpose'),
        ('/map_server/load_map', '/robot2/map_server/load_map'),
        ('/global_costmap/clear_entirely_global_costmap', '/robot2/global_costmap/clear_entirely_global_costmap'),
        ('/local_costmap/clear_entirely_local_costmap', '/robot2/local_costmap/clear_entirely_local_costmap'),
        ('/global_costmap/get_costmap', '/robot2/global_costmap/get_costmap'),
        ('/local_costmap/get_costmap', '/robot2/local_costmap/get_costmap'),
        ('/reached_goal', '/robot2/reached_goal'),
        ('/toggle_wait', '/robot2/toggle_wait'),
        ('/global_path', '/robot2/global_path'),
        ('/other_reached_goal', '/robot1/reached_goal')
    ]
    
    r1_controller = Node(
            package = 'robot_ui',
            executable = 'robot_ui',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'robot_name': 'robot1'},
                {
                    'initial_pose': LaunchConfiguration('r1_initial_pose'),
                    'goal_pose': LaunchConfiguration('r1_goal_pose')
                }
            ],
            remappings=remaps_r1
        )
        
    r2_controller = Node(
        package = 'robot_ui',
        executable = 'robot_ui',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'robot_name': 'robot2'},
            {
                'initial_pose': LaunchConfiguration('r2_initial_pose'),
                'goal_pose': LaunchConfiguration('r2_goal_pose')
            }
        ],
        remappings=remaps_r2
    )
    
    return LaunchDescription([
        r1_initial_pose_argument,
        r1_goal_pose_argument,
        r1_controller,
        r2_initial_pose_argument,
        r2_goal_pose_argument,
        r2_controller
    ])
