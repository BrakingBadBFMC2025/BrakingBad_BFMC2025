from src.templates.threadwithstop import ThreadWithStop
import src.utils.messages.allMessages as allMessages
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender
from enum import Enum
import time


import socket




class threadPlanner(ThreadWithStop):
    """This thread handles Planner.
    Args:
        queueList (dictionary of multiprocessing.queues.Queue): Dictionary of queues where the ID is the type of messages.
        logging (logging object): Made for debugging.
        debugging (bool, optional): A flag for debugging. Defaults to False.
    """

    def __init__(self, queueList, logging, control_type,debugging=False):
        self.queuesList = queueList
        self.logging = logging
        self.debugging = debugging
        self.control_type = control_type


        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 9999))
        self.server.listen(1)


        self.control_command = {
            "type": 2,
            "arg1": 0,   #velocity
            "arg2": 0    #angle
        }
        self.main_command = {
            "type": 2,
            "arg1": 0,   #velocity
            "arg2": 0    #angle
        }


        self.behaviours = {
            "Stop": self.stop_behaviour,
            "Crosswalk": self.crosswalk_behaviour,
            "Parking": self.parking_behaviour,
            "Highway end": self.highway_exit_behaviour,
            "Highway entry": self.highway_entry_behaviour,
            "Priority": self.priority_behaviour,
            "Roundabout": self.roundabout_behaviour,
            "No entry": self.no_entry_behaviour,
            "One way": self.one_way_behaviour,
        }

        self.spotted_sign = {
            'label': "Unassigned",
            'x': 0,
            'y': 0,
            'z':0
        }

        self.subscribe()
        super(threadPlanner, self).__init__()


    #status variables
    #TODO
    class State(Enum):
        IDLE = 1
        IN_CITY = 2
        IN_HIGHWAY = 3 

    curr_state = State.IN_CITY

    #main command modifiers (behaviours)
    def canon_behaviour(self):
        #print("canon")
        if self.curr_state == self.State.IN_CITY:
            self.control_command['arg1'] = min(max(self.control_command['arg1'], 200),400) #confining speed
        elif self.curr_state == self.State.IN_HIGHWAY:
            self.control_command['arg1'] = min(600, max(self.control_command['arg1'], 400))
        self.control_command_pub.send(self.control_command)

    def stop_behaviour(self):
        print("stop behaviour", float(self.spotted_sign['z']))
        stopped=False
        if float(self.spotted_sign['z'])<=50:
            self.control_command['arg1'] = 50
            if float(self.spotted_sign['z'])<=35:
                self.control_command['arg1'] = 0
                stopped =True
            self.control_command_pub.send(self.control_command)
            
        else:
            self.canon_behaviour()
        print(self.control_command)

        if stopped:
            time.sleep(3)
            print("vehicle stopped")
        
        return


    def parking_behaviour(self):
        if float(self.spotted_sign['z'])<=35:
            self.control_command['arg1'] = 100 #slowing down 
                                                #and looking for a parking spot TODO

        self.control_command_pub.send(self.control_command)
        return

    def crosswalk_behaviour(self):
        if float(self.spotted_sign['z']) <=35:
            self.control_command['arg1'] = 50 #slowing down
                                                #is pedestrian ahead, stop TODO
        self.control_command_pub.send(self.control_command)
        return

    def priority_behaviour(self):
        self.canon_behaviour()
        

    def roundabout_behaviour(self):
        self.canon_behaviour()
        

    def highway_entry_behaviour(self):
        self.curr_state = self.State.IN_HIGHWAY
        self.canon_behaviour()
        

    def highway_exit_behaviour(self):
        if float(self.spotted_sign['z']) <= 80:
            self.curr_state = self.State.IN_CITY
            self.control_command['arg1']=100
            self.control_command_pub.send(self.control_command)
        self.canon_behaviour()
        

    def one_way_behaviour(self):
        self.canon_behaviour()
        

    def no_entry_behaviour(self):
        if float(self.spotted_sign['z']) <= 40:
            self.curr_state=self.State.IN_CITY
            self.control_command['arg1'] = -100
            self.control_command_pub.send(self.control_command)
            print('wpa')
        else:
            self.canon_behaviour()
        


    def run(self):
        time_interval = 0.5

        while self._running:
            self.main_command = self.main_command_sub.receive()


            data=0
            self.server.setblocking(False)  # Make the socket non-blocking
            try:
                client, addr = self.server.accept()
                data = client.recv(1024).decode()
                print("Turn Prediction:", data)
                client.close()
            except BlockingIOError:
                #print("[Planner] Connection Failed")
                pass  # No client is currently connecting

            command_ = 0 
            if (data == "Left Turn"):
                command_ = -50
            elif (data == "Right Turn"):
                command_ = 50
            else:
                command_ = 0 

            self.control_command['arg2'] = command_

            #if new command from main arrived, update, else go on with the previous
            if self.main_command is not None:
                self.control_command['arg1'] = self.main_command["arg1"]
                self.control_command['type'] = self.main_command["type"]

            #check for spotted signs #TODO make sure we can handle multiple at a time    
            self.spotted_sign = self.sign_sub.receive()
            
            if self.spotted_sign is None:
                self.canon_behaviour()
            else:
                #if there is a sign, call the appropriate behaviour to do whatever with the control_command    
                self.behaviours.get(self.spotted_sign['label'], self.canon_behaviour)()
                print("Spotted sign: ",self.spotted_sign['label'])

            time.sleep(time_interval)

    def subscribe(self):
        self.sign_sub = messageHandlerSubscriber(self.queuesList, allMessages.Sign, "lastOnly", True)
        self.main_command_sub = messageHandlerSubscriber(self.queuesList, allMessages.Main_Command, "lastOnly", True)



        self.control_command_pub = messageHandlerSender(self.queuesList, allMessages.Control_Command)


