source install/local_setup.bash
ros2 run bridge_qos_hack map_hack --ros-args -p "real_pub:=/tiago1/map" -p "fake_pub:=/tiago1/fake_map" -p "msg_type:=nav_msgs.msg.OccupancyGrid" &
ros2 run bridge_qos_hack map_hack --ros-args -p "real_pub:=/tiago2/map" -p "fake_pub:=/tiago2/fake_map" -p "msg_type:=nav_msgs.msg.OccupancyGrid"
