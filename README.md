# Software Architectures for Robotics (ROS2): TIAGo part

## <img src="https://user-images.githubusercontent.com/62358773/177950955-29f674e4-edee-4e5a-a7bc-fd5b10494816.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Software
Need to install:
* [_ROS2 galactic_](https://docs.ros.org/en/galactic/index.html) on Ubuntu 20.04;
* [_ROS1 noetic_](http://wiki.ros.org/noetic/Installation/Ubuntu) on Ubuntu 20.04;

## Comment the sources of the `.bashrc` file
Before starting we need to comment the `source` default command set in the `.bashrc` file. </br>
Follow these steps:
* `cd ~/.bashrc`;
* comment all the sources commands.

Then we need to install and build the ROS bridge repository. Before this we need to make a new workspace for the bridge. </br>
Follow these steps:
* `mkdir -p ~/ros_ws_bridge/src`;
* `cd ~/ros_ws_bridge/src`;
* `git clone https://github.com/ros2/ros1_bridge.git` to clone the entire repository;
* `cd ros1_bridge`
* `git checkout galactic` to switch to the galactic branch;
* `cd ~/ros_ws_bridge`;

## Build the bridge from source
We firstly need to source the ROS2 with:
* `source /opt/ros/galactic/setup.bash`;

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

Now we have to install all the requirements without the ROS bridge by </br>
* `colcon build --symlink-install --packages-skip ros1_bridge`

Open another shell in the same folder as before (type `cd ~/ros_ws_bridge`). </br>
Then we source the ROS1 and ROS2 with these commands:
* `source /opt/ros/noetic/setup.bash`;
* `source /opt/ros/galactic/setup.bash`;
* `source install/local_setup.bash`.

Now we start the building of the repository by: </br>
* `colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure`

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
