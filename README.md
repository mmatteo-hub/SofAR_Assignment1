# Software Architecture for Robotics: Assignment

## <img src="https://user-images.githubusercontent.com/62358773/177956928-fc3638f9-abf1-4cd8-8437-4733088c0c08.png" width="5%" height="5%"> Assignment specifications

### <img src="https://user-images.githubusercontent.com/62358773/174429243-6f4be968-e447-4a71-a49f-c4563931c7e5.png" width="4%" height="4%"> Navigation of two independent robots moving in an environmnet by avoiding collision between each other through precedence management

The assignmen concerns the possibility of driving two robots in a certain enviornment by setting a position they have to reach. The program has to manage the driving of the two robots by avoiding collision between each other robot or obstacles and managing a right of way between the agents acting.

Each robot involded need, of course, to localize properly itself in the environment.

### <img src="https://user-images.githubusercontent.com/62358773/174429200-def1a393-e34d-494f-978f-9591aa7d9e97.png" width="4%" height="4%"> Robot: TurtleBot3 Waffle

<img src="https://user-images.githubusercontent.com/62358773/174429109-3092766c-5d64-4d7b-8aae-002553882374.png" width="15%" height="15%">
The model of the robot used is the TurtleBot3 Waffle. TurtleBot3 is a small, affordable, programmable, ROS-based mobile robot for use in education, research, hobby, and product prototyping.
In the assignment we used two of them: they are provided with sensors all around the base platform and they are 3 DoF (Degree of Freedom) robots.

## <img src="https://user-images.githubusercontent.com/62358773/177950955-29f674e4-edee-4e5a-a7bc-fd5b10494816.png" width="5%" height="5%"> Softwares used
For the assignment we used different softwares to simulate the behaviour of the robots:
* _Gazebo_: used to simulate the real world the robots move into;
* _Rviz_: to simulate what the robots see when moving in the environment:
  * for _Rviz_ it is necessary that each robot has its own window, in fact for this software we need to open one window for each robot involved;
* _ROS2_(Robotics Operative System 2): this is the architecture used to communicate with the robots

## <img src="https://user-images.githubusercontent.com/62358773/175919787-96dfd662-af73-4ab6-a6ad-e7049ff1336e.png" width="5%" height="5%"> Program start
The program is composed of different nodes running at the same time so in order to start the simulation and simplify all the starting process we provided just one executable file to run by `./run.sh` shell command:
* the `.sh` file contains:
  * all the necessary _EXPORT_ commands for the simulation of:
    * Gazebo world;
    * Robot models;
  * all the `source` commands for the `.bashrc` file;
  * all the _launch_ commands for the nodes used. The nodes are launched in different terminals automatically:
    * _Nav2_ node which in turn starts many nodes;
    * _robot controller_ node for the _robot1_;
    * _robot controller_ node for the _robot2_;
    * _policy controller_ node;

## <img src="https://user-images.githubusercontent.com/62358773/177952062-a1a97fb2-a7fa-449e-90d3-bf1fae4da02f.png" width="5%" height="5%"> Theory behind the nodes

### <img src="https://user-images.githubusercontent.com/62358773/174600732-bb04a560-dffe-49b4-b2fd-2dd669c96ac5.png" width="4%" height="4%">

_Nav2_ is the main node running in the assignment and all the other nodes depend from it. It is responsible of the pose estimation of the two robots in the environment so that both robots can check the correspondences between the _real_ environment from Gazebo and the map of the environment and they an localize themselves even is the pose given is a wrong one.
Moreover, this node provide the possibility of give a goal to each robot so that they can compute a path and reach this goal.
In this case it is very important the provided _cost map_ of the environment which allows the robot avoide getting too close to the obstacles. In order to be safer in this way the robot is also provided a _local map_ which keeps it farer from the local obstacles: this is important when the environment is provided with dynamics obstacles that cannot be predicted by the global path the robot uses.

### <img src="https://user-images.githubusercontent.com/62358773/177954650-6e82424f-baa2-449a-877c-dd31886a8944.png" width="4%" height="4%"> Custom nodes

The main node we relate with is the _Nav2_ node. In addition we provided different nodes to communicate with the robots and to allow the robots to communicate between eachother. In particular:
* 2 nodes are used to drive the robot: in this case the two nodes are distinguish node, one referring to the first robot and the other referring to the other one. They are responsible of sending messages and commands to the robot to allow them to move into the environment independently.
* one node, _policy controller_, is resposible of the communication between the two robots. This node allow each robot to know the position of the other one and manages the way the robot move. 
In fact, to improve our assignment we gave the robot a certain priority (that can be changed):
  * the _robot1_ has higher priority;
  * the _robot2_ has lower priority;
  
  In this way, when the robots are in a possible collision behaviour this node stops the lower priority robot until the path is free again.

### <img src="https://user-images.githubusercontent.com/62358773/177957979-a9681dd1-55bf-4985-99c0-ead2c7289b1b.png" width="4%" height="4%"> General graph obtained
