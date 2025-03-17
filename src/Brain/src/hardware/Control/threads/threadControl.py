from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import (mainCamera)
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender
from src.hardware.Control.utils.PID_control import PID_control
from src.hardware.Control.utils.bezier_curve_calc import *
from src.hardware.Localization.utils.F_kin_ackerman import F_kin_ackerman
import src.utils.messages.allMessages as allMessages
import time
import math
import ast

MAX_STEERING = 250
MAX_SPEED = 500

Kp_steer = 0.704000
Kd_steer = 0.010422
arrival_threshold = 20

ctr_command = {
  "Time": 0,
  "Speed": 0,
  "Steer": 0
}

#time in seconds, speed in mm/s, steer in degrees
def parse_ctr_command(time, speed, steer):
    global ctr_command
    ctr_command["Time"] = int(time*10)
    ctr_command["Speed"] = int(speed)
    ctr_command["Steer"] = int(steer*10)
    return ctr_command
    
def get_ctr_command():
    global ctr_command
    time = ctr_command["Time"]/10
    speed = ctr_command["Speed"]
    steer = ctr_command["Steer"]/10
    return time, speed, steer



def LOG(msg):
    print("-> CONTROL LOG::",msg,"\n")

def arrived(x_distance, y_distance):
    dist = math.sqrt((x_distance)**2 + (y_distance)**2)
    if dist < arrival_threshold:
        return True
    else:
        return False
    


def degangle_to_steer(degangle):
    steer =0
    if degangle<0:
        steer = max(-MAX_STEERING, int(degangle))
    elif degangle>0:
        steer = min(MAX_STEERING, int(degangle))

    #quantizing to 5
    temp = int(steer/5)
    steer = int(temp*5)

    return steer

class threadControl(ThreadWithStop):
    """This thread handles Control.
    Args:
        queueList (dictionary of multiprocessing.queues.Queue): Dictionary of queues where the ID is the type of messages.
        logging (logging object): Made for debugging.
        debugging (bool, optional): A flag for debugging. Defaults to False.
    """


    def __init__(self, queueList, logging, debugging=False):
        self.queuesList = queueList
        self.logging = logging
        self.debugging = debugging
        self.controller = PID_control(MAX_STEERING)


        self.f_kin = F_kin_ackerman() # TODO this is to be replaced after localization package is complete

        self.subscribe()

        super(threadControl, self).__init__()

    def run(self): 
        global ctr_command

        time.sleep(2)
        if self.debugging:
            LOG("Control thread runnning")


        #waiting until engine starts before sending commands
        while(self.kl_sub.receive() is None):
            time.sleep(1)
       
        time.sleep(1)

        x_curr=0
        y_curr=0
        rot_curr=0

        x_distance=0 #in mm
        y_distance=0 #in mm
        rot_distance=0 #in degrees

        x_destination =0 #in mm
        y_destination=0 #in mm

        time_interval = 0.5 #in seconds
        vel =0 #in mm/s
        steer =0 #in degrees

        control_type=2
        arg1=0
        arg2=0

        waiting =1 # 1 if the car is expecting new command

        time.sleep(1)

        while(self.is_alive): #until manual shut down

            planner_command = self.planner_command_sub.receive()

            if planner_command is not None:
                control_type = planner_command["type"]
                arg1 = planner_command["arg1"]
                arg2 = planner_command["arg2"]


            if control_type==2: #polar coords control
                
                vel = arg1
                rot_distance = arg2
                
                steer = self.controller.calc_steer_on_angledeg(rot_distance)
                
                parse_ctr_command(time_interval, vel, steer)
                self.ctr_pub.send(ctr_command)
                LOG(ctr_command)

                time.sleep(time_interval)

            elif control_type==1: #eucl coods control
                x = arg1
                y = arg2

                LOG("N/A")
                time.sleep(time_interval)
                
            """
            if self.control_type==2:    #polar coords control 
                
                rot_distance = self.angle_sub.receive()
                distance = self.dist_sub.receive()

                if rot_distance is not None:
                    msg = "Following orientation: " + str(rot_distance) + " for distance: "+str(distance)
                    LOG(msg)

                    steer = self.controller.calc_steer_on_angledeg(rot_distance)
                    vel = self.controller.calc_speed_on_dist(distance, MAX_SPEED)

                parse_ctr_command(time_interval, vel, steer)
                self.ctr_pub.send(ctr_command)

                time.sleep(time_interval)
                
        
            elif self.control_type==1:  #euledian coords control

                #checking if there is a new move given
                #if yes then replace the old error and calc again
                dest_dict = self.dest_sub.receive()
                if(dest_dict is not None):
                    x_destination = int(dest_dict["x"])
                    y_destination = int(dest_dict["y"])
                    
                    #check if destination is reachable by car's model
                    if self.f_kin.move_validator(MAX_STEERING/10,x_destination,y_destination):
                        msg = "Moving to :"+str(x_destination)+", "+str(y_destination)
                        LOG(msg)

                        x_distance = x_destination
                        y_distance = y_destination
                        x_curr =0
                        y_curr=0
                        rot_curr=0
                        rot_distance = math.degrees(math.atan2(x_distance, y_distance))
                        waiting =0
                    else:
                        LOG("WARNING: Unreachable move.")
                        x_distance=0
                        y_distance=0
                        rot_distance =0
                        self.brake_pub.send(0.0)

                #if car is not at destination, execute movement
                if not arrived(x_distance, y_distance):
                    msg = "Distances to target: x:" +str(x_distance) + ", y:"+ str(y_distance) + ", rot:" + str(rot_distance)
                    LOG(msg)
                    
                    #calculating needed vel and steer to reach position
                    vel, steer = self.controller.calc(x_distance, y_distance, rot_distance, MAX_SPEED)
                    msg = "Calx: vel:" + str(vel) +", steer: " +str(steer)
                    LOG(msg)

                    #estimating expected displacement based on command
                    delta_x, delta_y, rot_curr = self.f_kin.get_deltas_from_commands(time_interval, vel, steer, rot_curr)

                    #updating distances (needed for the next loop of calculation) 
                    x_curr += delta_x
                    y_curr += delta_y

                    x_distance = x_destination - x_curr
                    y_distance = y_destination - y_curr
                    rot_distance = math.degrees(math.atan2(x_distance, y_distance)) - rot_curr

                    print("displacements: ",x_curr,y_curr,rot_curr)

                    #sending command
                    parse_ctr_command(time_interval, vel, steer)
                    self.ctr_pub.send(ctr_command)

                    # this is to avoid extreme overshoot
                    if(x_distance<-arrival_threshold or y_distance<-arrival_threshold):
                        x_distance=0
                        y_distance=0
                        rot_distance=0
                        x_curr=0
                        y_curr=0
                        rot_curr=0

                    time.sleep(time_interval) #TODO is that good practice tho?

                else:
                    if waiting ==0:
                        x_curr=0
                        y_curr=0
                        rot_curr=0
                        LOG("Expecting command...")
                        waiting =1
            """
        if self.debugging:
            LOG("CONTROL THREAD EXITING")
        
            

    def subscribe(self):
        """Subscribes to the messages you are interested in"""
        self.kl_sub = messageHandlerSubscriber(self.queuesList, allMessages.Klem, "lastOnly", True)
        self.imu_sub = messageHandlerSubscriber(self.queuesList, allMessages.ImuData, "lastOnly", True)
        self.planner_command_sub = messageHandlerSubscriber(self.queuesList, allMessages.Control_Command, "lastOnly", True)
        
        self.speed_pub = messageHandlerSender(self.queuesList, allMessages.SpeedMotor)
        self.steer_pub = messageHandlerSender(self.queuesList, allMessages.SteerMotor)
        self.brake_pub = messageHandlerSender(self.queuesList, allMessages.Brake)
        self.ctr_pub = messageHandlerSender(self.queuesList, allMessages.Control)

        pass
