import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher

def generate_launch_description():
    package_dir = get_package_share_directory('assignment_pkg')
    robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'tiago_robot.urdf')).read_text()

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'factory.wbt')
    )

    my_robot_driver = Node(
        package='assignment_pkg',
        executable='controller',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
        ]
    )

    obstacle_avoider = Node(
        package='assignment_pkg',
        executable='controller',
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