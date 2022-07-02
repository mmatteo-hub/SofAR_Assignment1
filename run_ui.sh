## Shell script to build and run the robot ui

# Exit when any command fails
set -e

# Sourcing the new builtworkspace
source install/local_setup.bash

ros2 run robot_ui robot_ui

