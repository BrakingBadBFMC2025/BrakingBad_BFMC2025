import math


# coordinates in mm, rotations in degrees
def bezier_curve_calc(curr_x, curr_y, set_x, set_y, set_rot, segments =10):
    #calculate control point
    ctr_x =0
    ctr_y=0
    curr_rot = 0 #car in initial position always ponting forward

    curr_rot_rads = math.radians(curr_rot)
    set_rot_rads = math.radians(set_rot)

    if set_rot == curr_rot:
        ctr_x = set_x
        ctr_y = set_y
    else:
        if set_rot_rads == curr_rot_rads + math.pi or set_rot_rads == curr_rot_rads - math.pi:
            set_rot_rads -= math.pi/16 #make the lines non parallel

        curr_lamda = math.tan(curr_rot_rads)
        set_lamda = math.tan(set_rot_rads)

        print(curr_lamda, set_lamda)

        b1 = curr_y - curr_lamda * curr_x
        b2 = set_y - set_lamda * set_x

        ctr_x = (b1-b2)/(set_lamda - curr_lamda)
        ctr_y = curr_lamda * ctr_x + b1

    #planning curve
    t=0
    curve = []
    while(t<1):
        a_x = ctr_x + (1-t)*(curr_x - ctr_x)
        a_y = ctr_y + (1-t) * (curr_y - ctr_y)

        b_x = ctr_x + (t)*(set_x - ctr_x)
        b_y = ctr_y + (t)*(set_y - ctr_y)

        c_x = int(a_x + t*(b_x - a_x))
        c_y = int(a_y + t*(b_y - a_y))

        curve.append((c_x, c_y))

        t += (1/(segments))

    return curve

