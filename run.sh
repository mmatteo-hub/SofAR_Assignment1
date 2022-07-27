## Shell script to build and run the simulation code

# Exit when any command fails
set -e

# Removing previous build folders
rm -r -f build/ devel/

# Building the entire workspace
catkin_make

# Sourcing the workspace
. devel/setup.bash

# Decreasing the replanning frequency to 100000 seconds so that for every goal,
# only a plan is computed and published by the planner.
rosrun dynamic_reconfigure dynparam set tiago1/move_base planner_frequency 0.00001
rosrun dynamic_reconfigure dynparam set tiago2/move_base planner_frequency 0.00001

# Launching the policy controller
gnome-terminal -- roslaunch policy_controller tiago_policy_controller.launch

# Waiting 5 seconds for policy controller to be set up
sleep 5

# Launching the robot controller which makes the robots go back and forth
gnome-terminal -- roslaunch robot_controller two_tiago_controllers.launch
