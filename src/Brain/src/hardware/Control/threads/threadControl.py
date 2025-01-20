from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import (mainCamera)
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender
import src.utils.messages.allMessages as allMessages
import time
import math

MAX_STEERING = 25
MAX_SPEED = 500
set_x=0
set_y=0

Kp_steer = 0.704000
Kd_steer = 0.010422
speed=0
steer_rads:float =0
steer_deg:float =0

ctr_command = {
  "Time": 0,
  "Speed": 0,
  "Steer": 0
}

def LOG(msg):
    print("-> CONTROL LOG::",msg,"\n")

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

    def __init__(self, queueList, logging, debugging=False, auto=False):
        self.queuesList = queueList
        self.logging = logging
        self.debugging = debugging
        self.auto = auto

        self.subscribe()
        super(threadControl, self).__init__()

    def run(self): 
        global set_x
        global set_y
        global ctr_command
        global steer_deg


        time.sleep(2)
        if self.debugging:
            LOG("Control thread runnning")


        #waiting until engine starts before sending commands
        while(self.kl_sub.receive() is None):
            time.sleep(1)


        if self.debugging:
            LOG("Engine enabled")
            LOG("Sending control commands...")
        
        
        #self.speed_pub.send("50")

        time.sleep(1)
        while(True):
            angle = self.trajectory_angle_sub.receive()
            steer=0
            if angle is not None:
                angle = math.degrees(angle)
                steer=degangle_to_steer(angle)
                #self.steer_pub.send(str(steer*10))
            
            print("angle recvd: ", angle)
            #print("steer: ",steer*10)
            

            time.sleep(0.5)

        
        self.speed_pub.send("0")


        if self.debugging:
            LOG("CONTROL THREAD EXITING")
        
            

    def subscribe(self):
        """Subscribes to the messages you are interested in"""
        self.kl_pub= messageHandlerSender(self.queuesList, allMessages.Klem)
        self.kl_sub = messageHandlerSubscriber(self.queuesList, allMessages.Klem, "lastOnly", True)

        self.speed_pub = messageHandlerSender(self.queuesList, allMessages.SpeedMotor)
        self.steer_pub = messageHandlerSender(self.queuesList, allMessages.SteerMotor)
        self.brake_pub = messageHandlerSender(self.queuesList, allMessages.Brake)
        self.ctr_pub = messageHandlerSender(self.queuesList, allMessages.Control)
        self.trajectory_angle_sub = messageHandlerSubscriber(self.queuesList, allMessages.Trajectory_angle_rads, "lastOnly", True)


        pass
