import os
import pathlib
import launch
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory, get_packages_with_prefixes
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from webots_ros2_driver.webots_launcher import WebotsLauncher


def generate_launch_description():
    optional_nodes = []
    package_dir = get_package_share_directory('webots_ros2_tiago')
    custom_package_dir = get_package_share_directory('sofar_assignment')
    world = LaunchConfiguration('world')
    mode = LaunchConfiguration('mode')   	
    use_rviz = LaunchConfiguration('rviz', default=True)
    use_nav = LaunchConfiguration('nav', default=True)
    robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'tiago_webots.urdf')).read_text()
    tiago1_control_params = os.path.join(custom_package_dir, 'resource', 'tiago1_control.yaml')
    tiago2_control_params = os.path.join(custom_package_dir, 'resource', 'tiago2_control.yaml')
    nav2_map = os.path.join(package_dir, 'resource', 'map.yaml')
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    # Webots
    webots = WebotsLauncher(
        world=PathJoinSubstitution([custom_package_dir, 'worlds', world]),
        mode=mode
    )

    tiago1_driver = Node(
        package='webots_ros2_driver',
        executable='driver',
        output='screen',
        additional_env= {'WEBOTS_ROBOT_NAME':'tiago1'},
        namespace= 'tiago1',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': use_sim_time},
            {'set_robot_state_publisher': True},
            tiago1_control_params
        ],
        remappings=[
            ('/tiago1/diffdrive_controller/cmd_vel_unstamped', '/tiago1/cmd_vel')
        ]
    )
    
    tiago2_driver = Node(
        package='webots_ros2_driver',
        executable='driver',
        output='screen',
        additional_env= {'WEBOTS_ROBOT_NAME':'tiago2'},
        namespace= 'tiago2',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': use_sim_time},
            {'set_robot_state_publisher': True},
            tiago2_control_params
        ],
        remappings=[
            ('/tiago2/diffdrive_controller/cmd_vel_unstamped', '/tiago2/cmd_vel')
        ]
    )


    controller_manager_timeout = ['--controller-manager-timeout', '100']
    controller_manager_prefix = 'python.exe' if os.name == 'nt' else ''

    use_deprecated_spawner_py = 'ROS_DISTRO' in os.environ and os.environ['ROS_DISTRO'] == 'foxy'
    
    tiago1_diffdrive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner' if not use_deprecated_spawner_py else 'spawner.py',
        output='screen',
        prefix=controller_manager_prefix,
        arguments=['diffdrive_controller', '-c', 'tiago1/controller_manager'] + controller_manager_timeout,
    )
    
    tiago2_diffdrive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner' if not use_deprecated_spawner_py else 'spawner.py',
        output='screen',
        prefix=controller_manager_prefix,
        arguments=['diffdrive_controller', '-c', 'tiago2/controller_manager'] + controller_manager_timeout,
    )
    
    tiago1_joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner' if not use_deprecated_spawner_py else 'spawner.py',
        output='screen',
        prefix=controller_manager_prefix,
        arguments=['joint_state_broadcaster', '-c', 'tiago1/controller_manager'] + controller_manager_timeout,
    )
    
    tiago2_joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner' if not use_deprecated_spawner_py else 'spawner.py',
        output='screen',
        prefix=controller_manager_prefix,
        arguments=['joint_state_broadcaster', '-c', 'tiago2/controller_manager'] + controller_manager_timeout,
    )
    
    tiago1_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace= 'tiago1',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
        ]
    )

    tiago2_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace='tiago2',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
        ]
    )

    footprint_publisher = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'base_footprint'],
    )

    rviz_config = os.path.join(get_package_share_directory('webots_ros2_tiago'), 'resource', 'default.rviz')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['--display-config=' + rviz_config],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=launch.conditions.IfCondition(use_rviz)
    )

    if 'nav2_bringup' in get_packages_with_prefixes():
        optional_nodes.append(IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')),
            launch_arguments=[
                ('map', nav2_map),
                ('use_sim_time', use_sim_time),
            ],
            condition=launch.conditions.IfCondition(use_nav)))
            
            

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='office.wbt',
            description='Choose one of the world files from `/sofar_assignment/world` directory'
        ),
        DeclareLaunchArgument(
            'mode',
            default_value='realtime',
            description='Webots startup mode, change it to `fast` to increase the simulation speed (no 3d rendering)'
        ),
        webots,
        rviz,
        tiago1_driver,
        tiago2_driver,
        tiago1_diffdrive_controller_spawner,
        tiago2_diffdrive_controller_spawner,
        tiago1_joint_state_broadcaster_spawner,
        tiago2_joint_state_broadcaster_spawner,
        tiago1_state_publisher,
        tiago2_state_publisher,
        footprint_publisher,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ] + optional_nodes)
