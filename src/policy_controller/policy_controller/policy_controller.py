import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from rcl_interfaces.msg import ParameterDescriptor
from rcl_interfaces.msg import ParameterType
from std_msgs.msg import String
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from action_msgs.srv import CancelGoal

class PolicyController(Node):

    def __init__(self):
        super().__init__('policy_controller')
        # Declaring some parameters to personalize the node
        self.declare_parameter('robot_names', descriptor=ParameterDescriptor(type=ParameterType.PARAMETER_STRING_ARRAY))
        self.declare_parameter('path_distance_threshold', 1.0)
        self.declare_parameter('robot_intersection_threshold', 1.0)
        self.declare_parameter('robots_distance_threshold', 1.5) 
        # Obtaining the parameters
        # These are the robots names ordered by priority
        self._robots = self.get_parameter('robot_names').get_parameter_value().string_array_value
        # This is the threshold for the path distance to compute the intersections
        pthreshold = self.get_parameter('path_distance_threshold').get_parameter_value().double_value
        self._pthreshold2 = pthreshold*pthreshold
        # This is the threshold for the distance between the robot and the intersection
        ithreshold = self.get_parameter('robot_intersection_threshold').get_parameter_value().double_value
        self._ithreshold2 = ithreshold*ithreshold
        # This is the threshold for the relative distance between the two robots
        rthreshold = self.get_parameter('robots_distance_threshold').get_parameter_value().double_value
        self._rthreshold2 = rthreshold*rthreshold
        
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
        self._intersection_pose = None
        # If the robot with minor priority is waiting
        self._robot_waiting = False
        
        # These are the topics where the plans are published when computed.
        # We need to subscribe to these topics to compute the intersections between the plans.
        self.sub_path0 = self.create_subscription(Path, self._robots[0]+'/received_global_plan', lambda msg: self.on_new_path_received(0, msg), 10)
        self.sub_path1 = self.create_subscription(Path, self._robots[1]+'/received_global_plan', lambda msg: self.on_new_path_received(1, msg), 10)
        # Once we have computed the intersections, we need to know where the two robots are.
        self.create_subscription(Odometry, self._robots[0]+'/odom', lambda msg: self.on_robot_odom(0, msg), 10)
        self.create_subscription(Odometry, self._robots[1]+'/odom', lambda msg: self.on_robot_odom(1, msg), 10)
        

    def on_new_path_received(self, robot_id, msg):
        if robot_id == 0:
            self.destroy_subscription(self.sub_path0)
        else :
            self.destroy_subscription(self.sub_path1)
            
        # Creating a new empty list
        poses = []
        # Appending only the positions
        for pose_stamped in msg.poses :
            poses.append(pose_stamped.pose.position)
        # Storing the positions list
        self._paths[robot_id] = poses
        
        # A new path is received, so the old data is not valid anymore
        self._intersection_pose = None
        # TODO if the robot stopped, it should start again
        
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
            for i0 in range(len(self._paths[0])) :
                # Two points from the the two paths
                p0 = self._paths[0][i0]
                p1 = self._paths[1][i1]
                # Checking for intersection
                if dist2(p0, p1) < self._pthreshold2 :
                    self._intersection_pose = p1
                    break
            else:
                continue
            break
                    
        # Logging next intersection if found
        if not self._intersection_pose == None :
            pose_str = "( "+str(self._intersection_pose.x)+" , "+str(self._intersection_pose.y)+" )"
            self.get_logger().info("Found intersection at: "+pose_str+" .")
        else :
            self.get_logger().info("Found no intersection")
        
        
    def on_robot_odom(self, robot_id, msg):
        # Storing the last received position of the corresponding robot
        self._poses[robot_id] = msg.pose.pose.position
        
        # Check if the robot should wait
        if robot_id == 1 and not self._intersection_pose == None :
            self._maybe_stop_robot(robot_id)
            return
        
        # Check if the robot should restart moving
        if robot_id == 0 and self._robot_waiting == True :
            self._maybe_restart_robot()
            return
            

    def _maybe_stop_robot(self, robot_id):
        # Check if the robot is near enough to the intersection
        # And then if the two robots are near enough
        if dist2(self._poses[robot_id], self._intersection_pose) < self._ithreshold2 :
            self.get_logger().info("Intersection pose reached")
            if dist2(self._poses[0], self._poses[1]) < self._rthreshold2 :
                self.get_logger().info("Starting to wait...")
                # Canceling the goal of the robot with the specified id
                stop_service = self.create_client(CancelGoal, self._robots[robot_id]+'/navigate_to_pose/_action/cancel_goal')
                stop_service.call_async(CancelGoal.Request())
                # Flag for making the robot restart
                self._robot_waiting = True
         
           
    def _maybe_restart_robot(self, robot_id):
        # Check if the two robots are far enough
        if dist2(self._poses[0], self._poses[1]) > self._rthreshold2 + 0.5 :
            # TODO Send the previous goal to the old robot
            self._robot_waiting = False
                
                

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
