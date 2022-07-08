## Shell script to build and run the simulation code

# Exit when any command fails
set -e

# Removing previous build folders
rm -r -f build/ install/ log/

# Building the entire workspace
colcon build

# Sourcing the new builtworkspace
source install/local_setup.bash

WORLD_MODELS=$(pwd)"/src/my_bringup/worlds/models"
TURTLEBOT_MODELS="/opt/ros/galactic/share/turtlebot3_gazebo/models"

# Comunicating to Gazebo where to find additional models
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$TURTLEBOT_MODELS:$WORLD_MODELS
# Setting the turtlebot3 model type
export TURTLEBOT3_MODEL=waffle

# Launching the simulation
gnome-terminal -- ros2 launch my_bringup two_tb3_simulation_launch.py

# Launching the policy controller
gnome-terminal -- ros2 launch policy_controller policy_controller_launch.py

# Launching the robots controller
gnome-terminal -- ros2 launch robot_controller two_robot_controller_launch.py



