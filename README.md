# Software Architectures for Robotics (ROS2): Assignment

<img src="https://user-images.githubusercontent.com/62358773/158238820-f418cc09-4227-4afc-9c31-1705dfb64f5a.png" width="5%" height="5%"> Professor: [Simone Macciò](https://github.com/SimoneMacci0)

<img src="https://user-images.githubusercontent.com/62358773/158238810-c5dcb486-ba24-4b35-87de-39a54e88f36b.png" width="5%" height="5%"> Students: [Matteo Maragliano](https://github.com/mmatteo-hub), [Mattia Musumeci](https://github.com/IlMusu), [Daniele Martino Parisi](https://github.com/DaniPari99)

## <img src="https://user-images.githubusercontent.com/62358773/177956928-fc3638f9-abf1-4cd8-8437-4733088c0c08.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Assignment specifications

### <img src="https://user-images.githubusercontent.com/62358773/174429243-6f4be968-e447-4a71-a49f-c4563931c7e5.png" width="4%" height="4%">&nbsp;&nbsp;&nbsp;Navigation of two independent robots moving in an environmnet by avoiding collision between each other through precedence management

This assignment is focused on developing an architecture that allows to navigate two robots inside a realistic environment while avoiding collisions. This behaviour has been obtained by developing a **"policy controller"** that dedices which, between the two robots, has the right of way in the case of a foreshadowed collision.

### <img src="https://user-images.githubusercontent.com/62358773/174429200-def1a393-e34d-494f-978f-9591aa7d9e97.png" width="4%" height="4%">&nbsp;&nbsp;&nbsp;TurtleBot3 Waffle Robot

<img src="https://user-images.githubusercontent.com/62358773/174429109-3092766c-5d64-4d7b-8aae-002553882374.png" width="15%" height="15%"> </br>
The software has been tested with the [TurtleBot3 Waffle](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/) robot model, which is a small, affordable and programmable, ROS-based mobile robot for use in education, research, hobby, and product prototyping. This robot can run SLAM algorithms to build a map of the environment and use it to localize itself while navigating.


## <img src="https://user-images.githubusercontent.com/62358773/177950955-29f674e4-edee-4e5a-a7bc-fd5b10494816.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Software
For the assignment we used different softwares to simulate the behaviour of the robots:
* _Gazebo_: a 3-dimensional physics simulator used in robotics.

* _Rviz_: a visualization tool that allows inspect the simulation.

* _ROS2 Galactic_ ([documentation](https://docs.ros.org/en/galactic/index.html)): an open-source and meta-operating system which provides a set of libraries and tools for building robot applications.

* _Nav2_  ([documentation](https://navigation.ros.org/)): an architecture built on top of the ROS2 environment which aims to find a safe way to drive a mobile robot from point A to point B. 


###  <img src="https://user-images.githubusercontent.com/62358773/174600732-bb04a560-dffe-49b4-b2fd-2dd669c96ac5.png" width="4%" height="4%">&nbsp;&nbsp;&nbsp;Nav2
The Nav2 project is the spiritual successor of the ROS Navigation Stack and aims to find a safe way to drive a mobile robot from point A to point B. This includes a complete dynamic path planning, avoid obstacles, compute velocities for motors and structure recovery behaviours.</br>
This architecture uses behaviour trees (BT) to call modular servers to complete an action: compute a path, control effort, recovery, or any other navigation related action. These are each saparate nodes that communicate with the behaviour three over a ROS action server.</br>
Using the BT modules provided by Nav2 it is possible to localize the robot in the environment and make it navigate to its destination, or goal, even if the localization is not perferct.</br>
The collision avoidance behaviour is obtained using two costmaps: a global costmap which includes all the objects in the enviroment and a local costmap which is updated more frequently and keeps track only of the objects near the robot.

## <img src="https://user-images.githubusercontent.com/62358773/175919787-96dfd662-af73-4ab6-a6ad-e7049ff1336e.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Program Start
To obtain the derised behaviour it is necessary to launch all the previously mentioned software with the correct parameters. Therefore, in order to start the program we provide a shell script file, called `run.sh` ([code](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/run.sh)), which automatically builds the packages and runs all the necessary tools.
More precisely, this file contains:
  * all the necessary `EXPORT` commands for:
    * Gazebo world models;
    * Robot models;
  * all the necessary `source` commands;
  * all the _launch_ commands for the nodes used. 

The nodes are launched in different terminals automatically:
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
