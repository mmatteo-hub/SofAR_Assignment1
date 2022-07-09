# Software Architectures for Robotics (ROS2): Assignment

<img src="https://user-images.githubusercontent.com/62358773/158238820-f418cc09-4227-4afc-9c31-1705dfb64f5a.png" width="5%" height="5%"> Professor: [Simone Macciò](https://github.com/SimoneMacci0)

<img src="https://user-images.githubusercontent.com/62358773/158238810-c5dcb486-ba24-4b35-87de-39a54e88f36b.png" width="5%" height="5%"> Students: [Matteo Maragliano](https://github.com/mmatteo-hub), [Mattia Musumeci](https://github.com/IlMusu), [Daniele Martino Parisi](https://github.com/DaniPari99)

## <img src="https://user-images.githubusercontent.com/62358773/177956928-fc3638f9-abf1-4cd8-8437-4733088c0c08.png" width="5%" height="5%"> Assignment specifications

### <img src="https://user-images.githubusercontent.com/62358773/174429243-6f4be968-e447-4a71-a49f-c4563931c7e5.png" width="4%" height="4%"> Navigation of two independent robots moving in an environmnet by avoiding collision between each other through precedence management

The assignment concerns the possibility of driving two robots in a certain enviornment by setting a position they have to reach. The program has to manage the driving of the two robots by avoiding collision between each other robot or obstacles and managing a right of way between the agents acting.

Each robot involded needs, of course, to localize properly itself in the environment.

### <img src="https://user-images.githubusercontent.com/62358773/174429200-def1a393-e34d-494f-978f-9591aa7d9e97.png" width="4%" height="4%"> Robot: TurtleBot3 Waffle

<img src="https://user-images.githubusercontent.com/62358773/174429109-3092766c-5d64-4d7b-8aae-002553882374.png" width="15%" height="15%">
The model of the robot used is the TurtleBot3 Waffle. TurtleBot3 is a small, affordable, programmable, ROS-based mobile robot for use in education, research, hobby, and product prototyping.
In the assignment we used two of them: they are provided with sensors all around the base platform and they are 3 DoF (Degree of Freedom) robots.

## <img src="https://user-images.githubusercontent.com/62358773/177950955-29f674e4-edee-4e5a-a7bc-fd5b10494816.png" width="5%" height="5%"> Softwares used
For the assignment we used different softwares to simulate the behaviour of the robots:
* _Gazebo_: used to simulate the real world the robots move into;
* _Rviz_: to simulate what the robots see when moving in the environment:
  * for _Rviz_ it is necessary that each robot has its own window, in fact for this software we need to open one window for each robot involved;
* _ROS2_(Robot Operating System 2) galactic ([documentation](https://docs.ros.org/en/galactic/index.html)): this is the architecture used to communicate with the robots and let them to communicate between each other.

## <img src="https://user-images.githubusercontent.com/62358773/175919787-96dfd662-af73-4ab6-a6ad-e7049ff1336e.png" width="5%" height="5%"> Program start
The program is composed of different nodes running at the same time so in order to start the simulation and simplify all the starting process we provided just one executable file to run by `./run.sh` shell command ([code](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/run.sh)):
* the `.sh` file contains:
  * all the necessary `EXPORT commands for the simulation of:
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

_Nav2_, ([documentation](https://navigation.ros.org/index.html)), is the main node running in the assignment and all the other nodes depend from it. It is responsible of the pose estimation of the two robots in the environment so that both robots can check the correspondences between the _real_ environment from Gazebo and the map of the environment; they can and have to localize themselves even if the pose given is a wrong one.
Moreover, this node provides the possibility of giving a goal to each robot so that they can compute a path and reach this goal. In this case it is very important the provided _cost map_ of the environment which allows the robot avoid getting too close to the obstacles. In order to be safer in this way the robot is also provided a _local map_ which keeps it farer from the local obstacles: this is important when the environment is provided with dynamics obstacles that cannot be predicted by the global path the robot uses.

### <img src="https://user-images.githubusercontent.com/62358773/177954650-6e82424f-baa2-449a-877c-dd31886a8944.png" width="4%" height="4%"> Custom nodes

The main node we relate with is the _Nav2_ node. In addition we provided different nodes to communicate with the robots and to allow the robots to communicate between each other. In particular:
* 2 nodes, _robot controller_ are used to drive the robot ([src](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/src/robot_controller/robot_controller/robot_controller.py)), each one with a proper namespace: in this case the two nodes are distinguish node, one referring to the first robot and the other referring to the other one. They are responsible of sending messages and commands to the robot to allow them to move into the environment independently.
* one node, _policy controller_ ([src](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/src/policy_controller/policy_controller/policy_controller.py)), is resposible of the communication between the two robots. This node allows each robot to know the position of the other one and to manage the way the robot move. 
In fact, to improve our assignment we gave the robot a certain priority (that can be changed):
  * the _robot1_ has higher priority;
  * the _robot2_ has lower priority;
  
  In this way, when the robots are in a possible collision behaviour this node stops the lower priority robot until the path is free again.

* one node, _robot navigator_ ([src](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/src/my_commander/my_commander/robot_navigator.py)) which provides an API that handles all the ROS2 and Action Server tasks for you such that you can focus on building an application leveraging the capabilities of _Nav2_. This node is the _Simple Commander API_ ([link](https://navigation.ros.org/commander_api/index.html)) provided by the _Nav2_ adapted to this to fit the problem with multiple robots.

### <img src="https://user-images.githubusercontent.com/62358773/177957979-a9681dd1-55bf-4985-99c0-ead2c7289b1b.png" width="4%" height="4%"> General graph obtained

Here we present a schematic graph of the architecture used in the assigment. We showed only the most relevant topics, actions and servers used and we highlighted the nodes developed.

All the minor nodes that _Nav2_ implies and runs by itself are not shown here for sake of clarity and it is meant included in the general _Nav2_ node.

In the graph the arrow goes the same direction of the message passed by the topic, action or server used.

<p align="center">
 <img src="https://user-images.githubusercontent.com/62358773/178008913-62c0766e-f504-4158-947e-a9588727666e.jpeg" width="70%" height="70%">
</p>
