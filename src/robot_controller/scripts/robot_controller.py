#! /usr/bin/env python2

import rospy
import actionlib

from std_msgs.msg import Empty as EmptyMsg
from std_srvs.srv import SetBool, SetBoolResponse
from geometry_msgs.msg import Pose
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class RobotController():
    def __init__(self):
        # Intializing this node
        rospy.init_node('robot_controller')
        # Obtaining the parameters
        initial_pose = array_to_pose(rospy.get_param('~initial_pose'))
        goal_pose = array_to_pose(rospy.get_param('~goal_pose'))

        # Intializing some variables
        self._current_path = None
        self._reached_goal = True
        self._is_stopped = True
        self._other_reached_goal = True
        # The goal posees of the robot
        self._poses = [initial_pose, goal_pose]
        # The current goal (which has been reached) is the initial position
        self._goal_index = 0

        # Publisher for when the robot reached the goal
        self._srg_pub = rospy.Publisher('reached_goal', EmptyMsg, queue_size=10)
        # Subscriber for when the other robot reached the goal
        self._org_sub = rospy.Subscriber('other_reached_goal', EmptyMsg, self.other_reached_goal)

        # Service for temporarely stopping the robot
        self._twait_srv = rospy.Service('toggle_wait', SetBool, self.request_toggle_wait)

        # Creates an ActionClient for the move_base architecture
        self._move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)


    def other_reached_goal(self, msg):
        # Storing the information
        self._other_reached_goal = True
        rospy.loginfo('The other robot reached its goal!')
        # If this robot already reached the goal, now that the other also
        # reached the goal, this robot needs to restart
        self.check_and_set_next_goal()
    

    def request_toggle_wait(self, request):
        # The robot is stopped but the previous path is stored so that
        # it is possible to start following it again later on
        if request.data == True :
            self.wait_at_current_position()
            rospy.loginfo("Started waiting!")
        else :
            self.move_to_next_goal()
            rospy.loginfo("Stopped waiting!")
            
        # Setting the response
        return SetBoolResponse(True, "")
        

    def check_and_set_next_goal(self):
        # To set a new goal, the previous one must be reached
        if not self._reached_goal or not self._other_reached_goal:
            return
        
        # Reinitializing logic
        self._reached_goal = False
        self._other_reached_goal = False
        
        # Setting the next goal
        self._goal_index = (self._goal_index+1)%2
        # Following the path until the goal is reached
        self.move_to_next_goal()


    def wait_at_current_position(self):
        # Check if robot is already stopped
        if self._is_stopped :
            return False
        # Forcing the robot to stop
        self._is_stopped = True
        self._move_base.cancel_all_goals()
        return True


    def move_to_next_goal(self):
        # Check if robot is already moving
        if not self._is_stopped :
            return False
        # Making the robot follow the current path
        self._is_stopped = False
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.pose = self._poses[self._goal_index]
        # Communicating the action to the server
        # Waiting until server exists
        self._move_base.wait_for_server()
        self._move_base.send_goal(goal, done_cb=self.on_goal_reached)
        rospy.loginfo("Set a new goal!")
        return True

    def on_goal_reached(self, status, result):
        # This callback is called also if the robot starts to wait
        # In the case the robot is waiting, nothing needs to be done here
        if self._is_stopped == True :
            return

        rospy.loginfo("Goal reached!")

        # The robot reached the goal, so it is now stopped
        self._is_stopped = True
                    
        # Publishing on the reached goal topic
        self._srg_pub.publish(EmptyMsg())
        # Marking this robot as reached the goal
        self._reached_goal = True
        
        # Even if this robot just reached the goal, it might need to restart
        # because the other robot already reached the goal
        self.check_and_set_next_goal()



def array_to_pose(string):
    # Parses the string to an array
    array = string.strip()[1:-1].split(',')
    # Contains both position and orientation
    pose = Pose()
    pose.position.x = float(array[0])
    pose.position.y = float(array[1])
    pose.position.z = float(array[2])
    pose.orientation.x = float(array[3])
    pose.orientation.y = float(array[4])
    pose.orientation.z = float(array[5])
    pose.orientation.w = float(array[6])
    return pose

def main(argv=None):
    # Creating the RobotController node
    controller = RobotController()
    controller.check_and_set_next_goal()
    
    # Spinning the controller until interrupted
    try :
        rospy.spin()
    except KeyboardInterrupt:
        # When interrupted
        pass


if __name__ == '__main__':
    main()
