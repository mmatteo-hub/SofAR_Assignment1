import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped

class RobotUI(Node):

    def __init__(self):
        super().__init__('robot_ui')
        # Creating a helper for the navigation stack
        self._nav2 = BasicNavigator()
        
    def prompt_commands(self):
        self.get_logger().info("Choose one of the possible commands:")
        self.get_logger().info("1. Set robot namespace.")
        self.get_logger().info("2. Set robot goal.")
        
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
        
        
        
        
def main(args=None):
    # Initializing the Ros2 library
    rclpy.init(args=args)

    # Creating to RobotUI
    robot_ui = RobotUI()
    # Spinning to prevent exit
    rclpy.spin(robot_ui)


if __name__ == '__main__':
    main()
