import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Range 
from geometry_msgs.msg import Twist 

MAX_RANGE = 0.15

class ObstacleAvoider(Node):
    def __init__(self):
        super().__init__('obstacle_avoider')
        self.__publisher = self.create_publisher(Twist, 'cmd_vel', 1)
        self.create_subscription(Range, 'left_sensor', self.__left_sensor_callback, 1)
        self.create_subscription(Range, 'right_sensor', self.__right_sensor_callback, 1)
        
    def __left_sensor_callback(self, message):
        self.__left_sensor_value = message.range
        
    def __right_sensor_callback(self, message):
        self.__right_sensor_value = message.range
        
        command_message = Twist()

        if self.__left_sensor_value < 0.9*MAX_RANGE and self.__right_sensor_value < 0.9*MAX_RANGE:
            command_message.angular.z = -2.0
            command_message.linear.x = -0.1
        
        elif self.__right_sensor_value > 0.9*MAX_RANGE and self.__left_sensor_value < 0.9*MAX_RANGE:
            command_message.angular.z = -2.0

        elif self.__right_sensor_value < 0.9*MAX_RANGE and self.__left_sensor_value > 0.9*MAX_RANGE:
            command_message.angular.z = 2.0

        else:
            command_message.linear.x = 0.1
            
        self.__publisher.publish(command_message)
        
def main(args=None):
    rclpy.init(args=args)
    avoider=ObstacleAvoider()
    rclpy.spin(avoider)
    avoider.destroy_node()
    rclpy.shutdown()
        
if __name__ == '__main__':
    main()