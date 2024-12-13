#include "controllers/Steering_controller.hpp"


#define MAX_STEERING 20.0

using namespace std;

Steering_PID_Controller::Steering_PID_Controller(){
    index =0;
    rot_error=0;
    x_error=0;
    y_error=0;
    steer=0;
    curr_rot=0;
    curr_x=0;
    curr_y=0;
    set_x=0;
    set_y=0;


    YAML::Node config = YAML::LoadFile("src/control/config/steer_PID_params.yaml");

    Kp = config["pid"]["Kp"].as<double>();
    Ki = config["pid"]["Ki"].as<double>();
    Kd = config["pid"]["Kd"].as<double>();
}

void Steering_PID_Controller::update_coords_rotation(double x, double y, double r){
    curr_y = y;
    curr_x = x;
    curr_rot = r;
}

void Steering_PID_Controller::set_destination(double x, double y){
    set_x = x;
    set_y = y;
}

void Steering_PID_Controller::update_rot_error_history(){
    if(index==9)
        index=-1;
    rot_error_history[++index] = rot_error;
}

double Steering_PID_Controller::get_rot_error_sum(){
    double sum=0;
    for(int i=0; i<sizeof(rot_error_history)/4; i++){
        sum+=rot_error_history[i];
    }
    return sum;
}

double Steering_PID_Controller::calc_steering(bool print){
    update_rot_error_history(); //storing previous error value

    //calculating new error values
    x_error = set_x - curr_x; // distance in x axis
    y_error = set_y - curr_y; // distance in y axis

    double set_rot = atan2(y_error,x_error);
    rot_error = set_rot - curr_rot;

    if(abs(rot_error)>M_PI){
        if(rot_error<0){
            rot_error+=2*M_PI;
        }else{
            rot_error-=2*M_PI;
        }
    }

    //calculating steering
    steer = Kp*rot_error -Kd*steer; //requires tunning
    if(steer>0){
        steer = min(MAX_STEERING, (steer)*180/M_PI);
    }else{
        steer = max(-MAX_STEERING, (steer)*180/M_PI);
    }

    if(print)
        print_stats();

    return steer;
}

void Steering_PID_Controller::print_stats(){
    printf("->>> rot_dist: %f  -->> steering: %f\n", rot_error, steer);
}

