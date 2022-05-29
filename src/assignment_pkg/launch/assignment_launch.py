import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher

PACKAGE_NAME = 'assignment_pkg'

def generate_launch_description():
    package_dir = get_package_share_directory(PACKAGE_NAME)
    robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'tiago_robot.urdf')).read_text()

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'factory.wbt')
    )

    robot = Node(
        package='webots_ros2_driver',
        executable='driver',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
        ]
    )

    #controller = Node(
    #    package=PACKAGE_NAME,
    #    executable='controller',
    #)

    return LaunchDescription([
        webots,
        robot,
        #controller,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])