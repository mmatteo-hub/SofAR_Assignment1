import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher

PACKAGE_NAME = 'sofar_assignment_pkg'

def generate_launch_description():
    
    package_dir = get_package_share_directory(PACKAGE_NAME)
    
    # Loads the robot description file
    robot_description1 = pathlib.Path(os.path.join(package_dir, 'resource', 'robot1.urdf')).read_text()
    robot_description2 = pathlib.Path(os.path.join(package_dir, 'resource', 'robot2.urdf')).read_text()
    
    # Loads the world description file
    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'arena_4.wbt')
    )
    
    # Creates the driver Nodes
    driver_rbt1 = Node(
        package='webots_ros2_driver',
        executable='driver',
        namespace='rbt1',
        output='screen',
        additional_env={'WEBOTS_ROBOT_NAME': 'RBT_1'},
        parameters=[
            {'robot_description': robot_description1},
        ],
    )
    
    driver_rbt2 = Node(
        package='webots_ros2_driver',
        executable='driver',
        namespace='rbt2',
        output='screen',
        additional_env={'WEBOTS_ROBOT_NAME': 'RBT_2'},
        parameters=[
            {'robot_description': robot_description2},
        ]
    )
    

    return LaunchDescription([
        webots,
        driver_rbt1,
        driver_rbt2,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])
