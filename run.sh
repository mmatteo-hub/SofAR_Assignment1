## Shell script to build and run the code

# Removing previous build folders
rm -r build/ install/ log/

# Building the entire workspace
colcon build

# Sourcing the new builtworkspace
source install/local_setup.bash

# Comunicating to Gazebo where to find additional models
WORLD_MODELS=$(pwd)"/src/my_bringup/worlds/models"
TURTLEBOT_MODELS="/opt/ros/galactic/share/turtlebot3_gazebo/models"
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$TURTLEBOT_MODELS:$WORLD_MODELS
# Setting the turtlebot3 model type
export TURTLEBOT3_MODEL=waffle

echo $WORLD_MODELS

# Launching the simulation
ros2 launch my_bringup two_tb3_simulation_launch.py

ros2 launch robot_ui ui_launch.py
