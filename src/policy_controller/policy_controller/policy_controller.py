import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from std_msgs.msg import String
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from nav2_msgs.action import Wait
from geometry_msgs.msg import PoseStamped
from action_msgs.srv import CancelGoal

class PolicyController(Node):

    def __init__(self):
        super().__init__('policy_controller')
        
        # Initializing variables
        self._poses_1 = None
        self._poses_2 = None
        self._next_intersection_pose = None
        self._is_robot1_waiting = False
        
        # Receiving the global plan
        self.sub_r1 = self.create_subscription(Path, 'robot1/received_global_plan', self.on_robot1_path, 10)
        self.sub_r2 = self.create_subscription(Path, 'robot2/received_global_plan', self.on_robot2_path, 10)
        # Receiving the position of the robot
        self.sub_odom1 = self.create_subscription(Odometry, 'robot1/odom', self.on_robot1_odom, 10)
        self.sub_odom2 = self.create_subscription(Odometry, 'robot2/odom', self.on_robot2_odom, 10)
        # Wait client
        self._action_client = ActionClient(self, Wait, '/robo1/wait')
        

    def on_robot1_path(self, msg):
        # The global path is published only once
        # Therefore, the subscriber is not usefull anymore
        self.destroy_subscription(self.sub_r1)
        # Obtaining the poses
        self._poses_1 = PolicyController.parse_poses_from_msg(msg)
        print("Path from robot1 received")
        # Checks if the intersection can be computed and computes it
        self.check_and_intersect()
        
            
    def on_robot2_path(self, msg):
        # The global path is published only once
        # Therefore, the subscriber is not usefull anymore
        self.destroy_subscription(self.sub_r2)
        # Obtaining the poses
        self._poses_2 = PolicyController.parse_poses_from_msg(msg)
        print("Path from robot2 received")
        # Checks if the intersection can be computed and computes it
        self.check_and_intersect()
        
        
    def parse_poses_from_msg(msg):
        poses = []
        # Obtaining only the actual poses
        for pose_stamped in msg.poses :
            poses.append(pose_stamped.pose.position)
        return poses
        
        
    def check_and_intersect(self):
        # Check if both the paths are received
        if self._poses_1 == None or self._poses_2 == None :
            return
        print("Both path received")
        
        # Computing the intersections of the two paths
        intersections = []
        # Iterating for each segment in the two paths
        for id1 in range(0, len(self._poses_1)-1) :
            for id2 in range(0, len(self._poses_2)-1) :
                # A segment in path 1
                s1p1 = self._poses_1[id1]
                s1p2 = self._poses_1[id1+1]
                # A segment in path 2
                s2p1 = self._poses_2[id2]
                s2p2 = self._poses_2[id2+1]
                # Checking for intersection
                if intersect(s1p1, s1p2, s2p1, s2p2) :
                    intersections.append([id1, id2])
                  
        # Logging intersections  
        print("Found " + str(len(intersections)) + " intersections.")
        for inters in intersections :
            i1 = inters[0]
            i2 = inters[1]
            print("First segment:")
            print(str(self._poses_1[i1]) + "\n" + str(self._poses_1[i1+1]))
            print("Second segment:")
            print(str(self._poses_2[i2]) + "\n" + str(self._poses_2[i2+1]))
            
        # Storing the next intersection
        if len(intersections) > 0 :
            self._next_intersection_pose = intersections[0][0]
            
            
    def on_robot1_odom(self, msg):
        # Storing the last received position of the robot 1
        self._last_pose1 = msg.pose.pose.position
        
        # Check if there is a next intersection
        if self._next_intersection_pose == None :
            return
            
        self._check_and_wait_or_go()

    def on_robot2_odom(self, msg):
        # Storing the last received position of the robot 1
        self._last_pose2 = msg.pose.pose.position

    # NB. This always checks for robot1
    def _check_and_wait_or_go(self):
        # Check if the robot is near enough to the intersection
        if not self._is_robot1_waiting and is_same_pose_threshold(self._last_pose1, self._poses_1[self._next_intersection_pose], 0.16) :
            print("Intersection pose reached!")
            # Check if the two robots are near enough
            if is_same_pose_threshold(self._last_pose1, self._last_pose2, 0.25):
                print("Starting to wait...")
                # Making the robot 1 wait
                self._is_robot1_waiting = True
                _goal = Wait.Goal()
                _goal.time.sec = 3
                future = self._action_client.send_goal_async(_goal)
                future.add_done_callback(self._on_wait_finish)
                
    def _on_wait_finish(self, future):
        print("Finished waiting")
        self._is_robot1_waiting = False
        self._check_and_wait_or_go()

# Return true if line segments AB and CD intersect
def intersect(a,b,c,d):
    return ccw(a,c,d) != ccw(b,c,d) and ccw(a,b,c) != ccw(a,b,d)

# Checks if three points are in counter clockwise order
def ccw(a,b,c):
    return (c.y-a.y) * (b.x-a.x) > (b.y-a.y) * (c.x-a.x)

def is_same_pose_threshold(pos1, pos2, th2):
    f0 = pos1.x-pos2.x
    f1 = pos1.y-pos2.y
    dist2 = f0*f0+f1*f1
    return dist2 < th2

def main(args=None):
    rclpy.init(args=args)

    listener = PolicyController()
    rclpy.spin(listener)

    listener.destroy_node()
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()
