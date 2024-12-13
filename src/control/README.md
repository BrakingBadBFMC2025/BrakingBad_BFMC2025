# Control Package

## USAGE:

You need to run is as a node 
```
rosrun control movement_executor
```
    
You puslish a "std_mgs/Pose2D" type to the topic: `/control/movement_command`
Alternatively you may run overseer_node, which publishes coordinates given from command line  
```
rosrun control overseer
```

## DESCRIPTION:

Uses PID for both velocity and steering

will reach most coordinates, except those that need extreme steering

Has no way to reach specific orientation yet
