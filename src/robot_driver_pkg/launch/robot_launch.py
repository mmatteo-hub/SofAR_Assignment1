import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher

def generate_launch_description():
    package_name = 'robot_driver_pkg'
    package_dir = get_package_share_directory(package_name)
    
    # Loads the robot description file
    robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'robot.urdf')).read_text()
    
    # Loads the world description file
    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'arena_4.wbt')
    )
    
    # Creates the driver Node
    my_robot_driver = Node(
        package='webots_ros2_driver',
        executable='driver',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
        ]
    )
    
    # Creates the obstacle avoider Node
    obstacle_avoider = Node(
        package=package_name,
        executable='obstacle_avoider',   
    )
 
    return LaunchDescription([
        webots,
        my_robot_driver,
        obstacle_avoider,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])
