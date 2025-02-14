
#include "controllers/Steering_controller.hpp"
#include "controllers/Velocity_controller.hpp"
#include "geometry_msgs/Pose2D.h"

using namespace std;

Velocity_PID_Controller* vel_control;
Steering_PID_Controller* steer_control;
geometry_msgs::Pose2D dest_stats;
bool valid_move;



void curr_status_updater(utils::localisation data){
    vel_control->update_coords(data.posA, data.posB);
    steer_control->update_coords_rotation(data.posA, data.posB, -data.rotA); // WHY IS THE ROTATION INVERTED??!
}

void dest_coord_updater(geometry_msgs::Pose2D data){
    dest_stats = data;
    valid_move=true;
}



int main(int argc, char** argv){

    ros::init(argc, argv, "movement_executor");
    ros::NodeHandle n;

    vel_control = new Velocity_PID_Controller();
    steer_control = new Steering_PID_Controller();

    ros::Publisher commander = n.advertise<std_msgs::String>("/automobile/command", 1000);
    ros::Subscriber stats_updater = n.subscribe("/automobile/localisation", 1000, curr_status_updater);
    ros::Subscriber move_listener = n.subscribe("/control/movement_command", 1000, dest_coord_updater);


    ros::Rate loop_rate(10);

    std_msgs::String msg;

    double x,y;
    int counter;

        while(ros::ok()){

            ros::spinOnce();
            if(!valid_move){
                continue;
            }

            x = dest_stats.x;
            y = dest_stats.y;
            valid_move=false;

            vel_control->set_destination(x,y);
            steer_control->set_destination(x,y);

            printf("Moving to %f - %f\n", x,y);

            while(!vel_control->d_arrived() && ros::ok()){

                double velocity = vel_control->calc_velocity(true);

                double steering = steer_control->calc_steering(true);

                msg.data ="{\"action\":\"1\",\"speed\":" + to_string(velocity) + "}"; 
                commander.publish(msg);

                msg.data = "{\"action\":\"2\",\"steerAngle\":" + to_string(steering) + "}"; 
                commander.publish(msg);

                ros::spinOnce();

                if (valid_move)
                    break;
                
            }
            msg.data = "{\"action\":\"1\",\"speed\":0.0}";
            commander.publish(msg);
            ROS_INFO("\n==== MOVEMENT COMPLETE ====\n");
        }
    msg.data = "{\"action\":\"1\",\"speed\":0.0}";
    commander.publish(msg);
    return 1;
}

