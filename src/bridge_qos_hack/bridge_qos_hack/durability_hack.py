import rclpy
from rclpy.node import Node
from pydoc import locate

from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy
from rclpy.qos import QoSProfile, QoSReliabilityPolicy

class DurabilityHack(Node):
    
    def __init__(self):
        super().__init__('durability_hack')
        # This is the real publisher in ROS1
        real_pub = self.declare_parameter('real_pub', 'real_pub').get_parameter_value().string_value
        # This is the fake publisher that will be created in ROS2
        fake_pub = self.declare_parameter('fake_pub', 'fake_pub').get_parameter_value().string_value
        # This is the class of the message related to the topic
        TheClass = locate(self.declare_parameter('msg_type', 'msg_type').get_parameter_value().string_value)
        
        # The quality of service that will be held by the fake pub
        qos = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=10)
          
        # Creating the listener to the real publisher
        self.create_subscription(TheClass, real_pub, self.on_message, 10)

        # Creating the fake publisher
        self._publisher = self.create_publisher(TheClass, fake_pub, qos)
    
    def on_message(self, msg):
        print("Rooting new message!")
        # Publishing the message on the fake topic
        self._publisher.publish(msg)
        
        
def main(args=None):
    # Initializing ROS with the parameters
    rclpy.init(args=args)
    # Creating the RobotController node
    durability_hack = DurabilityHack()
    
    # Spinning the controller until interrupted
    try :
        rclpy.spin(durability_hack)
    except KeyboardInterrupt:
        # When interrupted
        durability_hack.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
