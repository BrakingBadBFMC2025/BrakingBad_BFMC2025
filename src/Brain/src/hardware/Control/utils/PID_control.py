import math

class PID_control:
    def __init__(self,vel_cap, steer_cap):
        self.Kp_v = 30.315000
        self.Kd_v = 0.100422
        self.Ki_v = 0.810000

        self.Kp_s = 0.704000
        self.Kd_s = 0.010422
        self.Ki_s = 0.810000

        self.vel_cap = vel_cap
        self.steer_cap = steer_cap/10
        self.vel =0
        self.steer =0

    # distance errors in mm, rotation error in degrees
    def calc(self, x_error, y_error, rot_error_deg):

        dist_error = math.sqrt((x_error)**2 + (y_error)**2)
        self.vel = min( (self.Kp_v * dist_error - self.Kd_v * self.vel) , self.vel_cap)
        self.vel = int(self.vel/50) * 50

        #wrapping around 2pi
        rot_error_deg = rot_error_deg%360
        if abs(rot_error_deg) >180:
            if rot_error_deg<0:
                rot_error_deg+=360
            else:
                rot_error_deg-=360
                
   
        #calculating steer in degrees - pid suboptimal tbh
        #self.steer = self.Kp_s * rot_error_deg - self.Kd_s * abs(self.steer)
        
        self.steer = rot_error_deg

        #enforcing steer_cap
        self.steer = max(-self.steer_cap, min(self.steer_cap, int(self.steer)))

        #quantizing to 5 bc the little shitbox cannot turn in smaller quantities
        self.steer = int(round(self.steer / 5) * 5)

        #print("CALCED VALUES: vel: ", self.vel, " steer: ", self.steer)
        return self.vel, self.steer
    
    def reset_values(self):
        self.vel=0
        self.steer=0
    