import math
import ast

class F_kin_ackerman:
    def __init__(self, axle_len=270):
        self.axle_len = axle_len # mm
        self.rot_rads = 0 #radians
        self.x=0 # mm
        self.y=0 # mm
        self.z=0 #mm
        self.dx=0
        self.dy=0
        self.dz =0
        self.ddx=0
        self.ddy=0
        self.ddz =0
        self.roll=0
        self.pitch=0
        self.yaw=0

    
    # time in seconds, speed in mm/s, steer and rotation in degrees
    def get_deltas_from_commands(self, time, speed, steer, curr_rot):
        steer_rads = math.radians(steer)
        curr_rot_rads= math.radians(curr_rot)
        if(steer!=0):
            curr_rot_rads = curr_rot_rads + ((speed/self.axle_len)*math.tan(steer_rads))*(time)
            #wrapping around pi
            curr_rot_rads = curr_rot_rads % (2*math.pi)
            if abs(curr_rot_rads)>math.pi:
                if curr_rot_rads<0:
                    curr_rot_rads+=2*math.pi
                else:
                    curr_rot_rads-=2*math.pi

        delta_x = int((speed*math.sin(curr_rot_rads))*time)
        delta_y = int((speed*math.cos(curr_rot_rads))*time)
        curr_rot_degrees = int(math.degrees(curr_rot_rads))

        return delta_x, delta_y, curr_rot_degrees

        
    def get_state_from_imu(self, imu_data:dict, time_interval):
        self.roll = float(imu_data['roll'] )
        self.pitch = float(imu_data['pitch'])
        self.yaw = float(imu_data['yaw'])

        ddx_prev = self.ddx
        self.ddx = float(imu_data['accelx'])
        ddy_prev = self.ddy
        self.ddy = float(imu_data['accely'])
        ddz_prev = self.ddz
        self.ddz = float(imu_data['accelz'])

        dx_prev = self.dx
        #self.dx = (ddx_prev + self.ddx)/2 * time_interval
        self.dx = dx_prev + (ddx_prev/2)*time_interval

        dy_prev = self.dy
        #self.dy = (ddy_prev + self.ddy)/2 * time_interval
        self.dy = dy_prev + (ddy_prev/2)*time_interval
        
        dz_prev = self.dz
        #self.dz = (ddz_prev + self.ddz)/2 * time_interval
        self.dz = dz_prev + (ddz_prev/2)*time_interval

        self.x = (dx_prev + self.dx)/2 * time_interval
        self.y = (dy_prev + self.dy)/2 * time_interval
        self.z = (dz_prev + self.dz)/2 * time_interval

        return self.x, self.y, self.z, self.yaw, self.pitch, self.roll


    #checks if the move is achievable by the car, returns True if it is
    #axle lenght and coordinates in mm, max_steering in degrees
    def move_validator(self, max_steering, target_x, target_y):
        max_steering_rads = math.radians(max_steering)

        #making sure the max_steering_rads sign is correct (meaning opposite of the target_x sign)
        if(max_steering_rads * target_x>0):
            max_steering_rads *= -1

        if max_steering_rads !=0:
            #instantaneous center of curvature location calculation:
            icc_x = -self.axle_len/math.tan(max_steering_rads) #distance of icc from the rear middle of the car 
            icc_y = 0
            radius = icc_x

            answer = False

            """
            fig, ax = plt.subplots()
            circle = plt.Circle((icc_x,icc_y), radius, color='blue', fill=False, linewidth=2)
            plt.scatter(icc_x,icc_y, color='black')
            plt.scatter(0,0,color = 'black')
            plt.scatter(target_x,target_y, color = 'green')
            ax.add_patch(circle)
            ax.set_xlim(-1000,1000)
            ax.set_ylim(-1000,1000)
            plt.show()

            """
            if ((target_x - icc_x)**2 + (target_y - icc_y)**2 >= radius**2) :
                answer = True    
        else:
            print("[move_validator]: INVALID MAX STEERING VALUE")
        
        return answer


    
    def reset_values(self):
        self.x=0
        self.y=0
        self.rot_rads= 0

