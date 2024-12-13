#ifndef STEERING_CONTROLLER_HPP
#define STEERING_CONTROLLER_HPP

#include "ros/ros.h"
#include "std_msgs/String.h"
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include "utils/localisation.h"
#include <unistd.h>
#include <yaml-cpp/yaml.h>

class Steering_PID_Controller{
    private:
        double rot_error; //rotation error
        double rot_error_history [10]; // array containing 10 previous erorr values
        double curr_rot;    //the rotation of the vehicle
        double curr_x, curr_y; //vehicle coordinates
        int index;  //used to iterate through the history array
        double steer;  //calculated steering value to be published
        double set_x, set_y;   //coords of destination
        double x_error, y_error; // distance in each axis
        double Kp, Ki, Kd; //PID params
        
        void update_rot_error_history();
        double get_rot_error_sum();
        void print_stats();

    public:
        Steering_PID_Controller();
        void update_coords_rotation(double x, double y, double r);  /** @brief updates the controller of the current state of the vehicle (coordinates and rotation)*/
        void set_destination(double x, double y);   /** @brief updates the controller of the point the vehicle is to go to */
        double calc_steering(bool print);       /** @brief calculates the steering using PID control @param print true for displaying calculated values */
};

#endif