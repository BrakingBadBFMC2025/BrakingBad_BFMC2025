#include "controllers/Velocity_controller.hpp"


Velocity_PID_Controller::Velocity_PID_Controller(){
    dist_error=0;
    curr_x=0; 
    curr_y=0;
    index =0;
    velocity=0;
    set_x=0;
    set_y=0;
    x_error=0;
    y_error=0;


    YAML::Node config = YAML::LoadFile("src/control/config/vel_PID_params.yaml");

    Kp = config["pid"]["Kp"].as<double>();
    Ki = config["pid"]["Ki"].as<double>();
    Kd = config["pid"]["Kd"].as<double>();
}


void Velocity_PID_Controller::update_coords(double x, double y){
    curr_y = y;
    curr_x = x;
}

void Velocity_PID_Controller::set_destination(double x, double y){
    set_x = x;
    set_y = y;
}

void Velocity_PID_Controller::update_dist_error_history(){
    if(index==9)
        index=-1;
    dist_error_history[++index] = dist_error;
}

double Velocity_PID_Controller::get_dist_error_sum(){
    double sum=0;
    for(int i=0; i<sizeof(dist_error_history)/4; i++){
        sum+=dist_error_history[i];
    }
    return sum;
}


double Velocity_PID_Controller::calc_velocity(bool print){
    update_dist_error_history(); //storing previous error value

    //calculating new error values
    x_error = set_x - curr_x; // distance in x axis
    y_error = set_y - curr_y; // distance in y axis
    dist_error = sqrt( pow(x_error,2) + pow(y_error,2) ); //the eucledian distance from the current coordinates to the set point

    //calculaing optimal velocity
    velocity = Kp*dist_error + Ki*0 - Kd*velocity;
    velocity = std::min(velocity,MAX_SPEED);

    if (print)
        print_stats();

    return velocity;
}

int Velocity_PID_Controller::d_arrived(){
    if(abs(set_x-curr_x)<=THRESHOLD && abs(set_y-curr_y)<=THRESHOLD)
        return 1;
    else 
        return 0;
}

void Velocity_PID_Controller::print_stats(){
    printf("->>> dist: x:%f y:%f  -->> calced vel: %f\n", x_error,y_error,velocity);
}


