

#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
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

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy


"""
Basic navigation demo to follow a given path
"""

def main():
    rclpy.init()

    navigator = BasicNavigator()
    
    # Go to our demos first goal pose
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = -2.0
    initial_pose.pose.position.y = -0.5
    initial_pose.pose.orientation.w = -1.5

    # Go to our demos first goal pose
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = navigator.get_clock().now().to_msg()
    goal_pose.pose.position.x = 2.0
    goal_pose.pose.position.y = 1.0
    goal_pose.pose.orientation.w = 0.0

    # Sanity check a valid path exists
    path = None
    while path == None:
        input("Prompt now")
        path = navigator.getPath(initial_pose, goal_pose)

    # Follow path
    navigator.followPath(path)

    i = 0
    while not navigator.isTaskComplete():
        # Printing only a feedback every 5
        # To not spam the console
        i += 1
        if not i%5 == 0 :
            continue
            
        # Do something with the feedback
        feedback = navigator.getFeedback()
        if feedback :
            print('Estimated distance: '+'{0:.3f}'.format(feedback.distance_to_goal))

    # Do something depending on the return code
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')

    #navigator.lifecycleShutdown()

    exit(0)


if __name__ == '__main__':
    main()
