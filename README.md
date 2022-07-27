# Software Architectures for Robotics: Assignment (ROS2 part)

<img src="https://user-images.githubusercontent.com/62358773/158238820-f418cc09-4227-4afc-9c31-1705dfb64f5a.png" width="5%" height="5%"> Professor: [Simone Macciò](https://github.com/SimoneMacci0)

<img src="https://user-images.githubusercontent.com/62358773/158238810-c5dcb486-ba24-4b35-87de-39a54e88f36b.png" width="5%" height="5%"> Students: [Matteo Maragliano](https://github.com/mmatteo-hub), [Mattia Musumeci](https://github.com/IlMusu), [Daniele Martino Parisi](https://github.com/DaniPari99)

## <img src="https://user-images.githubusercontent.com/62358773/177956928-fc3638f9-abf1-4cd8-8437-4733088c0c08.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Assignment specifications

### <img src="https://user-images.githubusercontent.com/62358773/174429243-6f4be968-e447-4a71-a49f-c4563931c7e5.png" width="4%" height="4%">&nbsp;&nbsp;&nbsp; Navigation of two independent robots moving in a known environmnet by avoiding collision between each other through precedence management

This assignment is focused on developing an architecture that allows two robots to navigate inside a real-world environment while avoiding collisions.
In particular, the robots must avoid collision between each other by giving the right of way according to a policy rule.
This behavior is obtained through a _policy controller_ which enforces the policy rule and decides which one, between the two robots, has the right of way in case they reach an intersection at the same time.

### <img src="https://user-images.githubusercontent.com/62358773/174429200-def1a393-e34d-494f-978f-9591aa7d9e97.png" width="4%" height="4%">&nbsp;&nbsp;&nbsp;TurtleBot3 Waffle Robot

<img src="https://user-images.githubusercontent.com/62358773/174429109-3092766c-5d64-4d7b-8aae-002553882374.png" width="15%" height="15%"> </br>
The software has been tested with the _TurtleBot3 Waffle_ ([specifications](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)) robot model, which is a small, affordable and programmable, ROS-based mobile robot for use in education, research, hobby, and product prototyping. This robot can run SLAM algorithms to build a map of the environment and use it to localize itself while navigating.


## <img src="https://user-images.githubusercontent.com/62358773/177950955-29f674e4-edee-4e5a-a7bc-fd5b10494816.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Software
For the assignment we used different softwares to simulate the behaviour of the robots:
* _Gazebo_: a 3-dimensional physics simulator used in robotics;

* _Rviz_: a visualization tool that allows inspect the simulation;

* _ROS2 Galactic_ ([documentation](https://docs.ros.org/en/galactic/index.html)): an open-source and meta-operating system which provides a set of libraries and tools for building robot applications;

* _Nav2_  ([documentation](https://navigation.ros.org/)): an architecture built on top of the ROS2 environment which aims to find a safe way to drive a mobile robot from point A to point B. 


###  <img src="https://user-images.githubusercontent.com/62358773/174600732-bb04a560-dffe-49b4-b2fd-2dd669c96ac5.png" width="4%" height="4%">&nbsp;&nbsp;&nbsp;Nav2
The Nav2 project is composed of a set of libraries which use ROS2 as the middleware to communicate with the hardware of the robot. The aim is to be able to provide an interface to be used to safely navigate a robot between two points. Using the Nav2 architecture it is possible to localize the robot in the environment and make it navigate to its destination, or goal, even if the localization is not perferct. </br>
In this context, the flow of task execution is defined by Behavior Trees which are, in fact, a tree structure of tasks to be completed: it creates a more human-understandable framework for defining a state machine application with many states.</br>
Generally, each node inside the Behavior Tree is linked to a ROS2 action server to complete an action: compute a path, control effort, recovery, or any other navigation related action.

## <img src="https://user-images.githubusercontent.com/62358773/175919787-96dfd662-af73-4ab6-a6ad-e7049ff1336e.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Program Start
To obtain the derised behaviour it is necessary to launch all the previously mentioned software with the correct parameters. Therefore, in order to start the program we provide a shell script file, called `run.sh` ([code](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/run.sh)), which automatically builds the packages and runs all the necessary tools.
More precisely, this file contains:
 * all the necessary `EXPORT` commands for:
   * Gazebo world models;
   * Robot models;
 * all the necessary `source` commands;
 * all the _launch_ commands for the nodes used. 
  
The nodes are launched in different terminals automatically:
 * The _Gazebo_, _Rviz_ and _Nav2_ processes and nodes;
 * Two _robot_controller_ nodes for the two robots inside the simulation;
 * The _policy_controller_ node.

## <img src="https://user-images.githubusercontent.com/62358773/177952062-a1a97fb2-a7fa-449e-90d3-bf1fae4da02f.png" width="5%" height="5%">&nbsp;&nbsp;&nbsp;Custom Nodes Implementation
As already said, the desired behaviour has been obtained through already existing nodes and custom nodes which need to be run simultaneously. In particular, the custom nodes are:
* The _robot_controller_ node  ([src](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/src/robot_controller/robot_controller/robot_controller.py)) comunicates with the Nav2 system to set or preempt a goal for the robot it is controlling. This is possible via the Simple Commander API ([documentaiton](https://navigation.ros.org/commander_api/index.html)) provided by Nav2 which implements all the basic functionalities to use the navigation.</br> 
Since our simulation contains two robots, two different instances of the controller node are created. More precisely, a robot_controller makes a robot move in loop between two speficied points.

* The _policy controller_ ([src](https://github.com/mmatteo-hub/SofAR_Assignment1/blob/main/src/policy_controller/policy_controller/policy_controller.py)) node is the responsible for handling the right of way of the two robots and, if needed, it comunicates with the robot_controller node to stop the related robot so that the other one is able to go through the intersection first. It is possible to specify the priority of the robots which are moving in the environment to define which robot has the right of way when crossing an intersection.

### <img src="https://user-images.githubusercontent.com/62358773/177957979-a9681dd1-55bf-4985-99c0-ead2c7289b1b.png" width="4%" height="4%">&nbsp;&nbsp;&nbsp;Implementation Graph

Here we present a schematic graph of the architecture used in the assigment in which are highlighted only the most relevant topics, services and actions used and also the developed nodes. A more complete schema would include also all the nodes, topics, services and actions that are defined inside the Nav2 architecture but we decided to not show them on purpose for sake of clarity.

In the graph, the arrows have the following meaning:
* topic: the message is sent to the node in the direction of the arrow;
* service: the service is provided by the node in the direction of the arrow;
* action: the action is provided by the node in the direction of the arrow.
&nbsp;
&nbsp;
<p align="center">
 <img src="https://user-images.githubusercontent.com/62358773/178280026-4e50c261-46f6-41dd-b40f-73fcbdb5a667.jpeg" width="90%" height="90%">
</p>
