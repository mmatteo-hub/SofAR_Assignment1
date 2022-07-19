# Software Architectures for Robotics (ROS2): TIAGo part

## <img src="https://user-images.githubusercontent.com/62358773/177950955-29f674e4-edee-4e5a-a7bc-fd5b10494816.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Software
Need to install:
* [_ROS2 galactic_](https://docs.ros.org/en/galactic/index.html) on Ubuntu 20.04;
* [_ROS1 noetic_](http://wiki.ros.org/noetic/Installation/Ubuntu) on Ubuntu 20.04;

## Comment the sources of the `.bashrc` file
Before starting we need to comment the `source` default command set in the `.bashrc` file. </br>
Follow these steps:
```
cd ~/.bashrc
```

* comment all the sources commands.

Then we need to install and build the ROS bridge repository. Before this we need to make a new workspace for the bridge. </br>
Follow these steps:
```
mkdir -p ~/ros_ws_bridge/src
cd ~/ros_ws_bridge/src`
git clone https://github.com/ros2/ros1_bridge.git` to clone the entire repository
cd ros1_bridge
git checkout galactic` to switch to the galactic branch
cd ~/ros_ws_bridge
```

### Prerequisites

In order to run the bridge you need to either:

* get [prebuilt binaries](https://github.com/ros2/ros2/releases) or
* build the bridge as well as the other ROS 2 packages from source.

After that you can run both examples described below.

For all examples you need to source the environment of the install space where the bridge was built or unpacked to.
Additionally you will need to either source the ROS 1 environment or at least set the `ROS_MASTER_URI` and run a `roscore`.

The following ROS 1 packages are required to build and use the bridge:
* `catkin`
* `roscpp`
* `roslaunch` (for `roscore` executable)
* `rosmsg`
* `std_msgs`
* as well as the Python package `rospkg`

To run the following examples you will also need these ROS 1 packages:
* `rosbash` (for `rosrun` executable)
* `roscpp_tutorials`
* `rospy_tutorials`
* `rostopic`
* `rqt_image_view`

## Build the bridge from source
We firstly need to source the ROS2 with:
```
source /opt/ros/galactic/setup.bash
```

Now we have to install all the requirements without the ROS bridge by </br>
```
colcon build --symlink-install --packages-skip ros1_bridge
```

Open another shell in the same folder as before (type `cd ~/ros_ws_bridge`). </br>
Then we source the ROS1 and ROS2 with these commands:
```
source /opt/ros/noetic/setup.bash
source /opt/ros/galactic/setup.bash
source install/local_setup.bash
```

Now we start the building of the repository by: </br>
```
colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure
```

## <img src="https://user-images.githubusercontent.com/62358773/175919787-96dfd662-af73-4ab6-a6ad-e7049ff1336e.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Run the ROS Bridge
* Shell A:
  * source ROS1 by: `source /opt/ros/noetic/setup.bash`;
  * start the master by: `roscore`.

* Shell B:
  * source ROS1 by: `source /opt/ros/noetic/setup.bash`;
  * source ROS2 by: `source /opt/ros/galactic/setup.bash`;
  * set the shell for ROS2 by: `source install/local_setup.bash`;
  * run the ROS bridge by: `ros2 run ros1_bridge dynamic_bridge`.

* Shell N: (just to run a node)
  * In order to run a node to be mapped from ROS1 to ROS2 or ROS2 to ROS1, just source the shell for the ROS version needed and run it.

## <img src="https://user-images.githubusercontent.com/62358773/179344919-f519fcd2-39b7-4b9e-b4d9-59d10090821d.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Connection between different devices
In order to connect two devices, one running ROS1 and another running ROS2 we have to follow few step:
* connect both devices to the same Wi-Fi network and:
  * open shell in each device and type `hostname -I`; the IP address that the shell will give will be used after;
* from another hell open the `.bashrc` in both devices by the command `gedit ~/.bashrc` and:
  * for ROS1:
    * sourcing the ROS1 by `source /opt/ros/noetic/setup.bash`;
    * export the ROS1 IP address by `export ROS_IP=IP_address`;
  * for ROS2:
    * sourcing the ROS2 by `source /opt/ros/galactic/setup.bash`;
    * exporting the IP address of the ROS1 device by `export ROS_MASTER_URI=http://IP_address:11311` where the 11311 is the ROS port;
    * export the ROS2 IP address by `export ROS_IP=IP_address`.

In case the ROS1 devices is a robot, so we cannot access directly its shell it is just sufficient to set the ROS2 device as explained before (the ROS_MASTER_URI can be taken from the Wi-Fi IP list) and starting the ROS bridge to start the communication.

## <img src="https://user-images.githubusercontent.com/62358773/179535296-ef4fc86d-8400-48d4-ac70-43f5a7643801.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Parameters

In order to run the parameter file from command line as soon as the rosbridge is launched we need to do: </br>
`ros2 run pkg_name node_name --ros-args --params-file ~path_to_file/params.yaml`

