#ifndef VELOCITY_CONTROLLER_HPP
#define VELOCITY_CONTROLLER_HPP

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


#define THRESHOLD 0.1
#define MAX_SPEED 0.3

class Velocity_PID_Controller{
    private:
        double dist_error; //distance error
        double dist_error_history [10];  //array containing 10 previous error values
        double curr_x, curr_y; //current_coordinates
        int index; //index in dist_error_history array
        double velocity; //calculated velocity, to be published
        double set_x, set_y;   //coordinatess of destination
        double x_error, y_error; // distance in each axis
        double Kp,Ki,Kd; //PID Parameters

        void update_dist_error_history(); // stores the latest distance value into an array replacing the oldest value
        double get_dist_error_sum(); //returns the sum of the 10 latest errors
        void print_stats(); // print total distance, x distance, y distance and velocity

    public:
        Velocity_PID_Controller();
        void update_coords(double x, double y);  /** @brief updates the controller of the current state of the vehicle (coordinates)*/
        void set_destination(double x, double y);   /** @brief updates the controller of the point the vehicle is to go to */
        double calc_velocity(bool print); /** @brief calculates the velocity using PID control @param print true for displaying calculated values */
        int d_arrived(); /** @brief @returns 1 if vehicle has arrived to destination (its distance is within a certain threshold)*/  
};

#endif