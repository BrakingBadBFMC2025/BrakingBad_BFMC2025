

class pid_steer_ctr:
    
    def __init__(relative = True):

        self.index =0
        self.rot_error=0
        self.x_error=0
        self.y_error=0
        self.steer=0
        self.curr.x =0
        self.curr.y=0
        self.curr.rot=0
        self.set_x=0
        self.set_y=0

        self.Kp= 30.315000
        self.Ki= 0.810000
        self.Kd= 0.100422

        