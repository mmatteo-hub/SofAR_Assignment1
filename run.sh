## Shell script to build and run the code

# take the global path of the workspace
MY_PATH=$(dirname "$0")
MY_PATH=$(cd "$MY_PATH" && pwd)
if [[ -z "$MY_PATH" ]] ; then
	exit 1
fi

# remove previous buildings
rm -r build/ install/ log/

# build the entire workspace
colcon build

# source the workspace
source install/local_setup.bash

# export the robot model
export TURTLEBOT3_MODEL=waffle

# export the model world for gazebo "${MY_PATH}/src"
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:"${MY_PATH}/src/nav2_bringup/bringup/worlds/models"

# launch the program of the
ros2 launch nav2_bringup two_tb3_simulation_launch.py
