import math

class PID_control:
    def __init__(self, steer_cap):
        self.Kp_v = 1.000000
        self.Kd_v = 0.100422
        self.Ki_v = 0.810000

        self.Kp_s = 1.000000
        self.Kd_s = 0.050422
        self.Ki_s = 0.810000

        self.steer_cap = int(steer_cap/10)
        self.vel =0
        self.steer =0


    def calc_speed_on_dist(self, distance, vel_cap):
        #calculating vel using PID
        self.vel = min( (self.Kp_v * distance - self.Kd_v * self.vel) , vel_cap)
        #quantizing to 50
        self.vel = int(self.vel/50)*50
        return self.vel

    def calc_steer_on_angledeg(self, angle_deg):
        #calculating steer using PID
        self.steer = (self.Kp_s * angle_deg) - (self.Kd_s * self.steer)
        #enforcing steer cap
        self.steer = max(-self.steer_cap, min(self.steer_cap, int(self.steer)))
        #quantizing to 5 bc the little shitbox cannot turn in smaller quantities
        self.steer = int(round(self.steer / 5) * 5)
        return self.steer

    # distance errors in mm, rotation error in degrees
    def calc(self, x_error, y_error, rot_error_deg, vel_cap):

        dist_error = math.sqrt((x_error)**2 + (y_error)**2)
        self.vel = min( (self.Kp_v * dist_error - self.Kd_v * self.vel) , vel_cap)
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
    