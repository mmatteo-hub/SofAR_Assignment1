# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Example for spawing multiple robots in Gazebo.

This is an example on how to create a launch file for spawning multiple robots into Gazebo
and launch multiple instances of the navigation stack, each controlling one robot.
The robots co-exist on a shared environment and are controlled by independent nav stacks
"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess, GroupAction,
                            IncludeLaunchDescription, LogInfo)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace

def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('my_bringup')
    launch_dir = os.path.join(bringup_dir, 'launch')

    # Names and poses of the robots
    robots = [
        {'name': 'tiago1'},
        {'name': 'tiago2'}
    ]


    autostart = LaunchConfiguration('autostart')

    # Declare the launch arguments

    declare_robot1_params_file_cmd = DeclareLaunchArgument(
        'tiago1_params_file',
        default_value=os.path.join(bringup_dir, 'params', 'nav2_multirobot_params_1.yaml'),
        description='Full path to the ROS2 parameters file to use for robot1 launched nodes')

    declare_robot2_params_file_cmd = DeclareLaunchArgument(
        'tiago2_params_file',
        default_value=os.path.join(bringup_dir, 'params', 'nav2_multirobot_params_2.yaml'),
        description='Full path to the ROS2 parameters file to use for robot2 launched nodes')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='True',
        description='Automatically startup the stacks')
        
    nav_instances_cmds = []
    for robot in robots:
        params_file = LaunchConfiguration(f"{robot['name']}_params_file")
        
        bringup_cmd_group = GroupAction([
            PushRosNamespace(robot['name']),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(launch_dir, 'navigation_bridge_launch.py')),
                launch_arguments={'namespace': robot['name'],
                                  'use_sim_time': 'True',
                                  'autostart': autostart,
                                  'params_file': params_file,
                                  'use_lifecycle_mgr': 'false',
                                  'map_subscribe_transient_local': 'true'}.items()),                              
        ])
        
        nav_instances_cmds.append(bringup_cmd_group)

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_robot1_params_file_cmd)
    ld.add_action(declare_robot2_params_file_cmd)
    ld.add_action(declare_autostart_cmd)

    for nav_instance in nav_instances_cmds:
        ld.add_action(nav_instance)

    return ld
