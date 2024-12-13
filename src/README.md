# Bosch Challenge

# Tutorial for installing Simulator for BFMC 2025.

## Install ROS-Noetic on Ubuntu 20.04
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```
```
sudo apt install curl
```
```
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```
```
sudo apt update
```
```
sudo apt install ros-noetic-desktop-full
```
```
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
```
## Instructions for setting up BFMC simulator.
1. ```cd ~/Documents```
2. ```git clone https://github.com/ECC-BFMC/Simulator.git```
3. ```cd ~/Documents/Simulator/```
4. ```catkin_make --pkg utils```
5. ```catkin_make```

## Edit .bashrc
Change {YOUR_USER} with your username
```
echo "export GAZEBO_MODEL_PATH="/home/{YOUR_USER}/Documents/Simulator/src/models_pkg:$GAZEBO_MODEL_PATH"" >> ~/.bashrc
```
```
echo "export ROS_PACKAGE_PATH="/home/{YOUR_USER}/Documents/Simulator/src:$ROS_PACKAGE_PATH"" >> ~/.bashrc
```
```
echo "source ~/Documents/Simulator/devel/setup.bash" >> ~/.bashrc 
```
Close all terminals and open a new one to run the sim.
```
roslaunch sim_pkg map_with_all_objects.launch
```

## Edit map_with_car_REC.launch
Replace line 9 with:
```
    <arg name="gui"          value="true"/>
```
Replace line 12 with:
```
<node pkg="sim_pkg" type="delay.sh" args="5 sim_pkg car_REC.launch" name="car_rec" output="screen"/>
```
