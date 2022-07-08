#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from rcl_interfaces.msg import ParameterType

from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from std_srvs.srv import SetBool

class PolicyController(Node):

    def __init__(self):
        super().__init__('policy_controller')
        # Declaring some parameters to personalize the node
        self.declare_parameter('robot_names', descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_STRING_ARRAY))
        self.declare_parameter('path_minimum_distance_threshold', 1.0)
        self.declare_parameter('robot_reach_intersection_threshold', 1.0)
        self.declare_parameter('intersections_minimum_distance_threshold', 0.8)
        self.declare_parameter('robots_minimum_distance_threshold', 2.0)
        # Obtaining the parameters
        # These are the robots names ordered by priority
        self._robots = self.get_parameter('robot_names').get_parameter_value().string_array_value
        # This is the threshold for the minimum path distance to compute the intersections
        pp_threshold = self.get_parameter('path_minimum_distance_threshold').get_parameter_value().double_value
        self._pp_threshold2 = pp_threshold*pp_threshold
        # This is the threshold for the distance between the robot and the intersection
        ri_threshold = self.get_parameter('robot_reach_intersection_threshold').get_parameter_value().double_value
        self._ri_threshold2 = ri_threshold*ri_threshold
        # This is the threshold for the relative distance between the two robots
        rr_threshold = self.get_parameter('robots_minimum_distance_threshold').get_parameter_value().double_value
        self._rr_threshold2 = rr_threshold*rr_threshold
        # This is the threshold for the minimum distance between the intersections
        ii_threshold = self.get_parameter('intersections_minimum_distance_threshold').get_parameter_value().double_value
        self._ii_threshold2 = ii_threshold*ii_threshold
        
        # There must be at least two robots specified
        if not self._robots or len(self._robots) != 2 :
            self.get_logger().error("Not enogh specified robots")
            return
        
        # Initializing variables
        # This contains the last recorded positions of the two robots.
        self._poses = [None, None]
        # This contains the paths of the two robots.
        self._paths = [[], []]
        # The next intersection positon
        self._intersections = []
        # If the robot with minor priority is waiting
        self._robot_waiting = False
        
        # These are the topics where the plans are published when computed.
        # We need to subscribe to these topics to compute the intersections between the plans.
        self.sub_path0 = self.create_subscription(Path, self._robots[0]+'/global_path', lambda msg: self.on_new_path_received(0, msg), 10)
        self.sub_path1 = self.create_subscription(Path, self._robots[1]+'/global_path', lambda msg: self.on_new_path_received(1, msg), 10)
        # Once we have computed the intersections, we need to know where the two robots are.
        self.create_subscription(Odometry, self._robots[0]+'/odom', lambda msg: self.on_robot_odom(0, msg), 10)
        self.create_subscription(Odometry, self._robots[1]+'/odom', lambda msg: self.on_robot_odom(1, msg), 10)
        # The service for stopping and restarting the robot with minor priotiry
        self.wait_srv = self.create_client(SetBool, self._robots[1]+'/toggle_wait')


    def on_new_path_received(self, robot_id, msg):
        # Creating a new empty list
        path = []
        # Appending only the positions
        for pose_stamped in msg.poses :
            path.append(pose_stamped.pose.position)
        # Storing the positions list
        self._paths[robot_id] = path
        
        # A new path is received, so the old data is not valid anymore
        self._intersections = []
        
        self.get_logger().info("Received path for "+self._robots[robot_id]+".")
        
        # Checks if the intersection can be computed and computes it
        self.check_and_intersect()


    def check_and_intersect(self):
        # Check if both the paths are received
        if not self._paths[0] or not self._paths[1] :
            return
        
        # Iterating for each segment in the two paths
        # NB. It is foundamentally important that the outer cycle is the one
        # related to the robot with the minor priority
        for i1 in range(len(self._paths[1])) :
            # A point from the path of robot 1
            p1 = self._paths[1][i1]
            # Check that p1 respects the minimum distance from the previous point
            if self._intersections :
                prev_intersection = self._intersections[len(self._intersections)-1]
                if dist2(p1, prev_intersection) < self._ii_threshold2 :
                    continue
            # Finding new intersections
            for i0 in range(len(self._paths[0])) :
                # A point from the path of robot 0
                p0 = self._paths[0][i0]
                # Checking for intersection
                if dist2(p0, p1) < self._pp_threshold2 :
                    self._intersections.append(p1)
                    # This point is an intersection, checking the next one
                    break
        
        # Logging the number of intersections found
        if self._intersections :
            self.get_logger().info("Found "+str(len(self._intersections))+" intersections.")
        else :
            self.get_logger().info("Found no intersection")


    def on_robot_odom(self, robot_id, msg):
        # Storing the last received position of the corresponding robot
        self._poses[robot_id] = msg.pose.pose.position
        
        if robot_id == 1 :
            # Check if the robot should stop and wait
            if self._robot_waiting == False and self._intersections :
                self._maybe_stop_robot(robot_id)
        else :
            # Check if the robot should restart
            if self._robot_waiting == True :
                self._maybe_restart_robot(robot_id)


    def _maybe_stop_robot(self, robot_id):
        # Check if the robot is near enough to the intersection
        # And then if the two robots are near enough
        if self.is_near_intersection(robot_id) :
            self.get_logger().info("Intersection pose reached")
            if dist2(self._poses[0], self._poses[1]) < self._rr_threshold2 :
                self.get_logger().info("Starting to wait...")
                # Canceling the goal of the robot with the specified id
                self.request_toggle_wait(True)
                # Flag for making the robot restart
                self._robot_waiting = True


    def _maybe_restart_robot(self, robot_id):
        # Check if the two robots are far enough
        if dist2(self._poses[0], self._poses[1]) > self._rr_threshold2 + 0.5 :
            self.get_logger().info("Finished waiting!")
            # Calling the service to make the robot start again
            self.request_toggle_wait(False)
            # Resetting the flag
            self._robot_waiting = False

            
    def is_near_intersection(self, robot_id):
        # Storing the robot position to optimize
        robot_pose = self._poses[robot_id]
        # Checks if the robot is near one of the intersections
        for intersection in self._intersections :
            if dist2(robot_pose, intersection) < self._ri_threshold2 :
                return True
        return False


    def request_toggle_wait(self, wait):
        # Creating the request
        request = SetBool.Request()
        request.data = wait
        # Sending the request
        self.wait_srv.call_async(request)



def main(args=None):
    # Initializing ROS with the parameters
    rclpy.init(args=args)
    # Creating the PolicyController node
    controller = PolicyController()
    
    # Spinning the controller until interrupted
    try :
        rclpy.spin(controller)
    except KeyboardInterrupt:
        # When interrupted
        controller.destroy_node()
        rclpy.shutdown()


def dist2(p0, p1) :
    f0 = p0.x-p1.x
    f1 = p0.y-p1.y
    return f0*f0+f1*f1


if __name__ == '__main__':
    main()



