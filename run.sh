## Shell script to build and run the code

# Exit when any command fails
set -e

# Removing previous build folders
rm -r -f build/ install/ log/

# The location of the custom behaviour tree
BT_FILE='default_nav_to_pose_bt_xml: "'$(pwd)'/src/my_bringup/trees/navigate_to_pose_w_replanning_and_recovery.xml"'
# The parameters files for the robot
ROBOT1_PARAMS_FILE="./src/my_bringup/params/nav2_multirobot_params_1.yaml"
ROBOT2_PARAMS_FILE="./src/my_bringup/params/nav2_multirobot_params_2.yaml"
PARAM_FILES=($ROBOT1_PARAMS_FILE $ROBOT2_PARAMS_FILE)

# Changing the parameters file to insert the correct location for the BT
for PARAMS_FILE in ${PARAM_FILES[@]}; do
    # Obtaining the line at which the BT is set
    LINE=$(grep -n "default_nav_to_pose_bt_xml:" $PARAMS_FILE | cut -d ":" -f 1)
    # If the line aready exists, it needs to be removed, other
    # the default line is the line 62.
    if [ $LINE != "" ]; then
        sed -i $LINE"d" $PARAMS_FILE
    else
        LINE="62"
    fi

    # Adding the line
    sed -i "62i\ \ \ \ $BT_FILE" $PARAMS_FILE
done

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
ros2 launch my_bringup two_tb3_simulation_launch.py



