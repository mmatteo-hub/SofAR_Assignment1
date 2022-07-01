import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped

class RobotUI(Node):

    def __init__(self):
        super().__init__('robot_ui')
        # Creating a helper for the navigation stack
        self._navigator_r1 = BasicNavigator()
        self._navigator_r2 = BasicNavigator()

    def _set_initial_poses(self):
        # Before using nav2, it is necesary to check that it is active        
        print("Waiting for Nav2 to be active...")
        self._navigator_r1.waitUntilNav2Active()
        self._navigator_r2.waitUntilNav2Active()
        print("Done")
        
        print("Setting initial poses... ")
        inital_pose_r1 = PoseStamped()
        inital_pose_r2 = PoseStamped()

        inital_pose_r1.header.frame_id = 'map'
        inital_pose_r2.header.frame_id = 'map'

        inital_pose_r1.header.stamp = self._navigator_r1.get_clock().now().to_msg()
        inital_pose_r2.header.stamp = self._navigator_r1.get_clock().now().to_msg()

        inital_pose_r1.pose.position.x = -5.0
        inital_pose_r1.pose.position.y = 1.0
        inital_pose_r1.pose.position.z = 0.1
        inital_pose_r1.pose.orientation.x = 0.0
        inital_pose_r1.pose.orientation.y = 0.0
        inital_pose_r1.pose.orientation.z = 0.0
        inital_pose_r1.pose.orientation.w = 1.0

        inital_pose_r2.pose.position.x = 5.0
        inital_pose_r2.pose.position.y = -1.0
        inital_pose_r2.pose.position.z = 0.1
        inital_pose_r1.pose.orientation.x = 0.0
        inital_pose_r2.pose.orientation.y = 0.0
        inital_pose_r2.pose.orientation.z = 0.0
        inital_pose_r2.pose.orientation.w = 1.0
        
        self._navigator_r1.setInitialPose(inital_pose_r1)
        self._navigator_r2.setInitialPose(inital_pose_r2)
        print("Done")

    def _show_commands(self):
        # Printing the possible commands to the user
        self.get_logger().info("Choose one of the possible commands:")
        self.get_logger().info("1. Set robot namespace.")
        self.get_logger().info("2. Set robot goal.")
        prompt = int(input())
        # Running the correct command
        if case == 1 :
            self._set_robot_namespace()
        elif case == 2 :
            self._set_robot_goal()
            
    def _set_robot_namespace(self):
        self.get_logger().info("Prompt the robot namespace:")
        self._namespace = input()
        
    def _set_robot_goal(self):

        self.get_logger().info("Prompt the x position:")
        posx = float(input())
        self.get_logger().info("Prompt the y position:")
        posy = float(input())
        self.get_logger().info("Prompt the orientation:")
        orientation = float(input())

        self._pose.position.x = posx
        self._pose.position.y = posy
        self._pose.orientation.w = orientation

        if self._namespace == "/robot1":
            self._navigator_r1.goToPose(self._pose)

            i = 0

            while not self._navigator_r1.isNavComplete():
                i = i + 1
                feedback = self._navigator_r1.getFeedback()
                if feedback and i % 5 == 0:
                    print('Distance remaining: ' + '{:.2f}'.format(feedback.distance_remaining) + ' m')

                    if(Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0)):
                        self._navigator_r1.cancelNav()
            
            result = self._navigator_r1.getResult()
            if result == TaskResult.SUCCEEDED:
                print('Goal succeeded')
            elif result == TaskResult.CANCELED:
                print('Goal canceled')
            elif result == TaskResult.FAILED:
                print('Goal failed')
            else:
                print('Invalid return status')

        elif self._namespace == "/robot2":
            self._navigator_r2.goToPose(self._pose)

            i = 0

            while not self._navigator_r2.isNavComplete():
                i = i + 1
                feedback = self._navigator_r2.getFeedback()
                if feedback and i % 5 == 0:
                    print('Distance remaining: ' + '{:.2f}'.format(feedback.distance_remaining) + ' m')

                    if(Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0)):
                        self._navigator_r2.cancelNav()
            
            result = self._navigator_r2.getResult()
            if result == TaskResult.SUCCEEDED:
                print('Goal succeeded')
            elif result == TaskResult.CANCELED:
                print('Goal canceled')
            elif result == TaskResult.FAILED:
                print('Goal failed')
            else:
                print('Invalid return status')

def main(args=None):
    # Initializing the Ros2 library
    rclpy.init(args=args)

    # Creating to RobotUI
    robot_ui = RobotUI()
    robot_ui._set_initial_poses()

    while(1):
        robot_ui._show_commands()

    # Spinning to prevent exit
    rclpy.spin(robot_ui)


if __name__ == '__main__':
    main()
