#include "ros/ros.h"
#include <iostream>
#include <unistd.h>
#include "geometry_msgs/Pose2D.h"


using namespace std;


int main(int argc, char** argv){

    ros::init(argc, argv, "manual_command");
    ros::NodeHandle n;

    ros::Publisher move_order = n.advertise<geometry_msgs::Pose2D>("/control/movement_command", 1000);

    double x,y;
    geometry_msgs::Pose2D dest_stats;

    while(ros::ok()){
        cout<<"enter coords: ";
        cin>>x>>y;

        dest_stats.x =x;
        dest_stats.y = y;

        move_order.publish(dest_stats);
    }
}