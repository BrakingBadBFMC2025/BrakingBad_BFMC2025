from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import (mainCamera)
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender
import src.utils.messages.allMessages as allMessages
from src.hardware.Localization.utils.F_kin_ackerman import F_kin_ackerman
import time
import math
import ast

class threadLocalization(ThreadWithStop):
    """This thread handles Localization.
    Args:
        queueList (dictionary of multiprocessing.queues.Queue): Dictionary of queues where the ID is the type of messages.
        logging (logging object): Made for debugging.
        debugging (bool, optional): A flag for debugging. Defaults to False.
    """

    def __init__(self, queueList, logging, debugging=False):
        super(threadLocalization, self).__init__()
        self.queuesList = queueList
        self.logging = logging
        self.debugging = debugging

        self.f_kin_model = F_kin_ackerman()

        self.subscribe()
        #self.imu_file = open("imu_readings.txt", "wt")
        

    def run(self):
    
        x =0.0
        y=0.0
        z=0.0
        time_start = time.time()
        while self._running:
            imu_str = self.imu_sub.receive()
            if imu_str is not None:
                imu_dict = ast.literal_eval(imu_str)
                curr_time = time.time()
                time_interval = curr_time - time_start
                
                delta_x, delta_y, delta_z, yaw, pitch, roll= self.f_kin_model.get_state_from_imu(imu_dict, float(time_interval))
                time_start = time.time()
                x += delta_x
                y += delta_y
                z += delta_z


        self.imu_file.close()


    def subscribe(self):
        self.imu_sub = messageHandlerSubscriber(self.queuesList, allMessages.ImuData, "lastonly", True)
        pass
