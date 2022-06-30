import rclpy
from rclpy import Node
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult, NavigationResult
from rclpy.duration import Duration
from geometry_msgs.msg import PoseStamped

class RobotUI(Node):

    def __init__(self):
        super().__init__('robot_ui')
        # Creating a helper for the navigation stack
        self._navigator_r1 = BasicNavigator()
        self._navigator_r2 = BasicNavigator()

        self._navigator_r1.waitUntilNav2Active()
        self._navigator_r2.waitUntilNav2Active()

    def _set_initial_pose(self):
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

    def _prompt_commands(self):
        self.get_logger().info("Choose one of the possible commands:")
        self.get_logger().info("1. Set robot namespace.")
        self.get_logger().info("2. Set robot goal.")
        
    def _set_robot_namespace(self):
        self.get_logger().info("Prompt the robot namespace [/robot1 or /robot2]:")
        self._namespace = input()
        
    def _set_robot_goal(self):

        self.get_logger().info("Prompt the x position:")
        posx = float(input())
        self.get_logger().info("Prompt the y position:")
        posy = float(input())
        self.get_logger().info("Prompt the orientation:")
        orientation = float(input())

        self._pose = [posx, posy, 0, 0, 0, 0, 1]

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
            if result == NavigationResult.SUCCEEDED:
                print('Goal succeeded')
            elif result == NavigationResult.CANCELED:
                print('Goal canceled')
            elif result == NavigationResult.FAILED:
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
            if result == NavigationResult.SUCCEEDED:
                print('Goal succeeded')
            elif result == NavigationResult.CANCELED:
                print('Goal canceled')
            elif result == NavigationResult.FAILED:
                print('Goal failed')
            else:
                print('Invalid return status')

def main(args=None):
    # Initializing the Ros2 library
    rclpy.init(args=args)

    # Creating to RobotUI
    robot_ui = RobotUI()

    while(1):
        robot_ui._prompt_commands()
        robot_ui._set_robot_namespace()
        robot_ui._set_robot_goal()

    # Spinning to prevent exit
    rclpy.spin(robot_ui)


if __name__ == '__main__':
    main()
