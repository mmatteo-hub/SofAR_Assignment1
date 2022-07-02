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
        
        self._poses_1 = None
        self._poses_2 = None
        self._next_intersection_pose = None
        # Creating a publisher that receives messages of type String
        # over a topic named 'topic' with the specified callback.
        self.sub_r1 = self.create_subscription(Path, 'robot1/received_global_plan', self.on_robot1_path, 10)
        self.sub_r2 = self.create_subscription(Path, 'robot2/received_global_plan', self.on_robot2_path, 10)
        # Cretting a publisher for each robot to store the goal pose
        self.sub_r1_goal = self.create_subscription(PoseStamped, '/robot1/goal_pose', self.robot1_goal, 10)
        self.sub_r2_goal = self.create_subscription(PoseStamped, '/robot2/goal_pose', self.robot2_goal, 10)
        # Odom subscribers
        self.sub_odom1 = self.create_subscription(Odometry, 'robot1/odom', self.on_robot1_odom, 10)
        self.sub_odom2 = self.create_subscription(Odometry, 'robot2/odom', self.on_robot2_odom, 10)
        # Wait client
        self._action_client = ActionClient(self, Wait, '/robo1/wait')

    def robot1_goal(self, msg):
        self._goal1_pose = msg.pose

    def robot2_goal(self, msg):
        self._goal2_pose = msg.pose
        

    def on_robot1_path(self, msg):
        # The global path is published only once
        # Therefore, the subscriber is not usefull anymore
        self.destroy_subscription(self.sub_r1)
        # Obtaining the poses
        self._poses_1 = PolicyController.parse_poses_from_msg(msg)
        print("Path from robot1 received\n")
        # Checks if the intersection can be computed and computes it
        self.check_and_intersect()
        
            
    def on_robot2_path(self, msg):
        # The global path is published only once
        # Therefore, the subscriber is not usefull anymore
        self.destroy_subscription(self.sub_r2)
        # Obtaining the poses
        self._poses_2 = PolicyController.parse_poses_from_msg(msg)
        print("Path from robot2 received\n")
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
        print("Both path received\n")
        
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
        print("Found " + str(len(intersections)) + " intersections.\n")
        for inters in intersections :
            i1 = inters[0]
            i2 = inters[1]
            print("First segment:\n")
            print(str(self._poses_1[i1]) + " " + str(self._poses_1[i1+1]) + "\n")
            print("Second segment:\n")
            print(str(self._poses_2[i2]) + " " + str(self._poses_2[i2+1]) + "\n")
            
        # Storing the next intersection
        if len(intersections) > 0 :
            self._next_intersection_pose = intersections[0][0]
            
            
    def on_robot1_odom(self, msg):
        if self._next_intersection_pose == None :
            return
            
        self._check_and_wait_or_go(msg.pose.pose.position)

    def on_robot2_odom(self, msg):
        self._last_pose2 = msg.pose
    
    def _on_wait_finish(self, future):
        self._check_and_wait_or_go(self.last_pose1)

    def _check_and_wait_or_go(self, current_pos):
        if is_same_pose_threshold(current_pos, self._poses_1[self._next_intersection_pose], 0.16) :
            print("Intersection pose reached!")
            self.last_pose1 = current_pos
            if is_same_pose_threshold(self.last_pose1, self._last_pose2, 0.25):
                _goal = Wait.Goal()
                _goal.sec = 3
                future = self._action_client.send_goal_async(_goal)
                future.add_done_callback(self._on_wait_finish)

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
