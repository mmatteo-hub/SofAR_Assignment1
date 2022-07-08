#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from rcl_interfaces.msg import ParameterType
from my_commander.robot_navigator import BasicNavigator, TaskResult

from std_msgs.msg import Empty as EmptyMsg
from std_srvs.srv import SetBool
from geometry_msgs.msg import PoseStamped, Pose, Point
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry

class RobotController(Node) :

    def __init__(self):
        super().__init__('robot_controller')
        self._navigator = None
        self._current_path = None
        self._reached_goal = True
        self._is_stopped = True
        self._other_reached_goal = True
        
        # Declaring some parameters
        self.declare_parameter('robot_name', 'name')
        self.declare_parameter('initial_pose', descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_DOUBLE_ARRAY))
        self.declare_parameter('goal_pose', descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_DOUBLE_ARRAY))
        
        # Obtaining the name of robot
        self._name = self.get_parameter('robot_name').get_parameter_value().string_value
        
        # Storing the two poses of interests inside an array
        initial_pose = array_to_pose(self.get_parameter('initial_pose').get_parameter_value().double_array_value)
        goal_pose = array_to_pose(self.get_parameter('goal_pose').get_parameter_value().double_array_value)
        self._poses = [initial_pose, goal_pose]
        # The current goal (which has been reached) is the initial position
        self._goal_index = 0
        
        # Publisher for the robot computed path
        self._path_pub = self.create_publisher(Path, 'global_path', 10)
        # Publisher for when the robot reached the goal
        self._srg_pub = self.create_publisher(EmptyMsg, 'reached_goal', 10)
        
        # Subscriber for when the other robot reached the goal
        self._org_sub = self.create_subscription(EmptyMsg, 'other_reached_goal', self.other_reached_goal, 10)
        
        # Service for temporarely stopping the robot
        self._twait_srv = self.create_service(SetBool, 'toggle_wait', self.request_toggle_wait)


    def other_reached_goal(self, msg):
        # Storing the information
        self._other_reached_goal = True
        self.get_logger().info("["+self._name+"] The other robot reached its goal!")
        # If this robot already reached the goal, now that the other also
        # reached the goal, this robot needs to restart
        self.check_and_set_next_goal()


    def request_toggle_wait(self, request, response):
        # The robot is stopped but the previous path is stored so that
        # it is possible to start following it again later on
        if request.data == True :
            self.wait_on_current_path()
            self.get_logger().info("["+self._name+"] Started waiting!")
        else :
            self.follow_current_path_until_goal()
            self.get_logger().info("["+self._name+"] Stopped waiting!")
            
        # Setting the response
        response.success = True
        response.message = ""
        return response


    def create_navigator(self):
        # Creating a Nav2 helper
        self._navigator = BasicNavigator(self._name)
        
        # Setting the initial position
        msg = PoseStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self._navigator.get_clock().now().to_msg()
        msg.pose = self._poses[0]
        self._navigator.setInitialPose(msg)
        
        # The Nav2 system is launched automatically, therefore it is necessary
        # to wait until all the functionalities are active
        self._navigator.waitUntilNav2Active()


    def check_and_set_next_goal(self):
        # To set a new goal, the previous one must be reached
        if not self._reached_goal or not self._other_reached_goal:
            return
        
        # Reinitializing logic
        self._reached_goal = False
        self._other_reached_goal = False
        
        # Setting the next goal
        self._goal_index = (self._goal_index+1)%2
        # Creating the path from the current pose to the goal pose
        self.create_new_path()
        # Following the path until the goal is reached
        self.follow_current_path_until_goal()

        
    def create_new_path(self):
        # The current position as a pose stamped
        cpose = PoseStamped()
        cpose.header.frame_id = 'map'
        cpose.header.stamp = self._navigator.get_clock().now().to_msg()
        cpose.pose = self._poses[(self._goal_index-1)%2]
        # The goal position as a pose stamped
        gpose = PoseStamped()
        gpose.header.frame_id = 'map'
        gpose.header.stamp = self._navigator.get_clock().now().to_msg()
        gpose.pose = self._poses[self._goal_index]
        
        # Obtaining the path
        self._current_path = self._navigator.getPath(cpose, gpose)
       
        # Publishing the path as new message
        msg = Path()
        msg.header.frame_id = 'map'
        msg.header.stamp = self._navigator.get_clock().now().to_msg()
        msg.poses = self._current_path.poses
        self._path_pub.publish(msg)
        
        self.get_logger().info("["+self._name+"] Published a new path!")


    def wait_on_current_path(self):
        # Check if robot is already stopped
        if self._is_stopped :
            return False
        # Forcing the robot to stop
        self._is_stopped = True
        self._navigator.cancelTask()
        
        # Destroying the rimer
        self.destroy_timer(self._timer)
        return True

        
    def follow_current_path_until_goal(self):
        # Check if robot is already moving
        if not self._is_stopped :
            return False
        # Making the robot follow the current path
        self._is_stopped = False
        self._navigator.followPath(self._current_path)
        
        # Creating a timer to check the status of the robot
        self._timer = self.create_timer(1, self.goal_check_callback)
        self._counter = 0
        return True
        
    
    def goal_check_callback(self):
        # If the task is not yet completed, do nothing
        if not self._navigator.isTaskComplete():
            # Clearing local cost map to prevent robot interaction
            self._counter += 1
            if self._counter % 3 == 0 :
                self._navigator.clearLocalCostmap()
            return
        
        self.get_logger().info("["+self._name+"] Goal reached!")
        
        # Destroying the timer
        self.destroy_timer(self._timer)
        # The robot reached the goal, so it is now stopped
        self._is_stopped = True
                    
        # Publishing on the reached goal topic
        self._srg_pub.publish(EmptyMsg())
        # Marking this robot as reached the goal
        self._reached_goal = True
        
        # Even if this robot just reached the goal, it might need to restart
        # because the other robot already reached the goal
        self.check_and_set_next_goal()

        
    def destroy_node(self):
        self._path_pub.destroy()
        self._srg_pub.destroy()
        self._org_sub.destroy()
        self._twait_srv.destroy()
        self._navigator.destroy_node()
        super().destroy_node()



def array_to_pose(array):
    # Contains both position and orientation
    pose = Pose()
    pose.position.x = array[0]
    pose.position.y = array[1]
    pose.position.z = array[2]
    pose.orientation.x = array[3]
    pose.orientation.y = array[4]
    pose.orientation.z = array[5]
    pose.orientation.w = array[6]
    return pose


def main(args=None):
    # Initializing ROS with the parameters
    rclpy.init(args=args)
    # Creating the RobotController node
    controller = RobotController()
    controller.create_navigator()
    controller.check_and_set_next_goal()
    
    # Spinning the controller until interrupted
    try :
        rclpy.spin(controller)
    except KeyboardInterrupt:
        # When interrupted
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
