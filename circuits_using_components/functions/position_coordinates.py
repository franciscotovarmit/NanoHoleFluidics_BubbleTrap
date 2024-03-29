#######################################
###Move path_2d_numpy function to a class later
### need to know how to pass the list of coodinates that this
###function generates to child cell positions
# Function to generate grid of coordinates where each object is placed
import numpy as np


def generate_positions(x,y,index):

    if index ==0:   #parallel
        m1, m2 = np.meshgrid(x, y)
        r = np.append(m1, m2)
        r.shape = 2, -1
        return r.T

    if index ==1:   #series
        l = len(x)
        offset = x[l-1]+2000#(x[1] - x[0]) * 0.5
        print 'off: ',offset
        #x[0] #0.0# (x[1] - x[0]) * 0.5  # if rows (y >1), then x[1]-x[0]
                                             #  but needs to get get lenght of list,
                                                # get value of last element   if
        xn = []
        yn = []
        for cnt in range(0, len(y)):
            for cntx in range(0, len(x)):
                yn.append(y[cnt])
                if cnt % 2 == 0:
                    xn.append(x[cntx] - offset)
                else:
                    xn.append(x[cntx])
        r = np.append(xn, yn)
        r.shape = 2, -1
        return r.T