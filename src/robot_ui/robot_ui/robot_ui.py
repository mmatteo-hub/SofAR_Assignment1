import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration

class RobotUI(Node):

    def __init__(self):
        super().__init__('robot_ui')
        # Creating a helper for the navigation stack
        self._nav2 = BasicNavigator()
        
    def prompt_commands():
        self.get_logger().info("Insert the namespace of the robot")
        
def main(args=None):
    # Initializing the Ros2 library
    rclpy.init(args=args)

    # Creating to RobotUI
    robot_ui = RobotUI()
    # Spinning to prevent exit
    rclpy.spin(robot_ui)


if __name__ == '__main__':
    main()
