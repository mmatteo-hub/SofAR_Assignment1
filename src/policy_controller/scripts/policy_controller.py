#! /usr/bin/env python2

import rospy
from time import sleep

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_srvs.srv import SetBool

class PolicyController():
    def __init__(self):
        # Intializing this node
        rospy.init_node('policy_controller')

        # These are the robots names ordered by priority
        self._robots = rospy.get_param('~robot_names', '[robot1, robot2]').strip()[1:-1].split(',')
        for i in range(len(self._robots)):
            self._robots[i] = self._robots[i].strip()
        # This is the threshold for the minimum path distance to compute the intersections
        pp_threshold = float(rospy.get_param('~path_minimum_distance_threshold', '1.0'))
        self._pp_threshold2 = pp_threshold*pp_threshold
        # This is the threshold for the distance between the robot and the intersection
        ri_threshold = float(rospy.get_param('~robot_reach_intersection_threshold', '1.0'))
        self._ri_threshold2 = ri_threshold*ri_threshold
        # This is the threshold for the relative distance between the two robots
        rr_threshold = float(rospy.get_param('~robots_minimum_distance_threshold', '2.0'))
        self._rr_threshold2 = rr_threshold*rr_threshold
        # This is the threshold for the minimum distance between the intersections
        ii_threshold = float(rospy.get_param('~intersections_minimum_distance_threshold', '0.1'))
        self._ii_threshold2 = ii_threshold*ii_threshold

        # There must be at least two robots specified
        if not self._robots or len(self._robots) != 2 :
            rospy.loginfo("Not enogh specified robots")
            return

        # Initializing variables
        # This contains the last recorded positions of the two robots.
        self._poses = [None, None]
        # This contains the paths of the two robots.
        self._paths = [[], []]
        # The next intersection positon
        self._intersections = []
        self._is_computing_intersections = False
        self._stop_computing_intersections = False
        # If the robot with minor priority is waiting
        self._robot_waiting = False

        # These are the topics where the plans are published when computed.
        # We need to subscribe to these topics to compute the intersections between the plans.
        self.sub_path0 = rospy.Subscriber(self._robots[0]+'/global_path', Path, lambda msg, argb: self.on_new_path_received(0, msg), 10)
        self.sub_path1 = rospy.Subscriber(self._robots[1]+'/global_path', Path, lambda msg, argb: self.on_new_path_received(1, msg), 10)
        # Once we have computed the intersections, we need to know where the two robots are.
        rospy.Subscriber(self._robots[0]+'/odom', PoseWithCovarianceStamped, lambda msg, argb: self.on_robot_odom(0, msg), 10)
        rospy.Subscriber(self._robots[1]+'/odom', PoseWithCovarianceStamped, lambda msg, argb: self.on_robot_odom(1, msg), 10)
        # The service for stopping and restarting the robot with minor priotiry
        self.wait_srv = rospy.ServiceProxy(self._robots[1]+'/toggle_wait', SetBool)


    def on_new_path_received(self, robot_id, msg):
        # Creating a new empty list
        path = []
        # Appending only the positions
        for pose_stamped in msg.poses :
            path.append(pose_stamped.pose.position)

        # Storing the positions list
        rospy.loginfo("Received path for "+self._robots[robot_id]+".")
        self._paths[robot_id] = path
        
        # Checks if the intersection can be computed and computes it
        # There is a small problem because the callbacks are executed on threads, therefore
        # it may happen that there are two instances of this function running at the same time.
        # This concurrency problem is solved using flags.
        self.check_and_intersect()


    def check_and_intersect(self):
        # Check if both the paths are received
        if not self._paths[0] or not self._paths[1] :
            return

        # Small check to prevent concurrency in computing intersections
        # A new path is available, therefore the old computation must be stopped
        if self._is_computing_intersections :
            self._stop_computing_intersections = True
            while self._is_computing_intersections :
                sleep(0.5)
            self._stop_computing_intersections = False

        # It is now computing the intersections
        self._is_computing_intersections = True
        # Creating new intersections
        self._intersections = []
        
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
                # Flag to avoid concurrency problems
                if self._stop_computing_intersections == True:
                    self._is_computing_intersections = False
                    return
                # A point from the path of robot 0
                p0 = self._paths[0][i0]
                # Checking for intersection
                if dist2(p0, p1) < self._pp_threshold2 :
                    self._intersections.append(p1)
                    # This point is an intersection, checking the next one
                    break

        # Here we stop the computation
        self._is_computing_intersections = False
        
        # Logging the number of intersections found
        if self._intersections :
            rospy.loginfo("Found "+str(len(self._intersections))+" intersections.")
        else :
            rospy.loginfo("Found no intersection")

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
            #rospy.loginfo("Intersection pose reached")
            if dist2(self._poses[0], self._poses[1]) < self._rr_threshold2 :
                rospy.loginfo("Starting to wait...")
                # Canceling the goal of the robot with the specified id
                self.request_toggle_wait(True)
                # Flag for making the robot restart
                self._robot_waiting = True


    def _maybe_restart_robot(self, robot_id):
        # Check if the two robots are far enough
        if dist2(self._poses[0], self._poses[1]) > self._rr_threshold2 + 0.2 :
            rospy.loginfo("Finished waiting!")
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
        # Sending the request
        self.wait_srv(wait)



def dist2(p0, p1) :
    f0 = p0.x-p1.x
    f1 = p0.y-p1.y
    return f0*f0+f1*f1


def main(argv=None):
    # Creating the RobotController node
    controller = PolicyController()
    
    # Spinning the controller until interrupted
    try :
        rospy.spin()
    except KeyboardInterrupt:
        # When interrupted
        pass


if __name__ == '__main__':
    main()
