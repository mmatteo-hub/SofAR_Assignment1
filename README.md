# Software Architecture for Robotics: Assignment

## <img src="https://user-images.githubusercontent.com/62358773/174429243-6f4be968-e447-4a71-a49f-c4563931c7e5.png" width="5%" height="5%">  Assignment specifications: Navigation of two independent robots avoiding collision
The assignment concerns the navigation of two independet robots in a given environment. The robots have to localize themselves into it and, as soon as they are given a goal, they have to reach it while avoiding obstacles.

### <img src="https://user-images.githubusercontent.com/62358773/174429200-def1a393-e34d-494f-978f-9591aa7d9e97.png" width="5%" height="5%"> Robot: TurtleBot3 Waffle
<img src="https://user-images.githubusercontent.com/62358773/174429109-3092766c-5d64-4d7b-8aae-002553882374.png" width="15%" height="15%">
The model of robot used is TurtleBot3 Waffle. TurtleBot3 is a small, affordable, programmable, ROS-based mobile robot for use in education, research, hobby, and product prototyping.
In the assignmet we used two of them: they are provided with sensors all around the base platform and they are 3 DoF (Degree of Freedom) robots.

## <img src="https://user-images.githubusercontent.com/62358773/175919787-96dfd662-af73-4ab6-a6ad-e7049ff1336e.png" width="5%" height="5%"> Program start
The program is composed of different nodes running at the same time so in order to start the simulation it is needed to follow these steps:
* `./run.sh`: to run the `.sh` file containing all the necessary _EXPORT_ for the simulation and the `source` commands for the `.bashrc` file;
* `ros2 launch `: to run the `.py` launch file;
* `ros2 launch `: to run the `.py` launch file the

In order to run the simulation we provided an executable `.sh` file, the command to use is: `./run.sh`
The file runs the Gazebo simulation and the two Rviz (one for each robot spawned).
It also provides the exports for the Gazebo map and the robot model for the simulations, in a way that the user does not have to insert them in the `.bashrc` file.

## Nav2
<p align="center">
  <img height="200" src="https://user-images.githubusercontent.com/62358773/174600732-bb04a560-dffe-49b4-b2fd-2dd669c96ac5.png"/>
</p>

_Nav2_ is the main node running in the assignment and all the other nodes depend from it.
It is responsible of the pose estimation of the two robots in the environment so that both robots can check the correspondences between the _real_ environment from Gazebo and the map of the environment and they an localize themselves even is the pose given is a wrong one.
Moreover, this node provide the possibility of given a goal to each robot so that they can compute a path and reach the goal.
In this case it is very important the _cost map_ of the environment which allows the robot avoide getting too close to the obstacles. In order to be more safe in this way the robot is also provided a _local map_ which keeps it farer from the local obstacles: this is important when the environment is provided with dynamics obstacles that cannot be predicted by the global path the robot uses.
