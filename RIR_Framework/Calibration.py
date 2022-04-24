#from curses.ascii import NL
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import minimize
from scipy import interpolate
from RIRsimulation import createRir
from mpl_toolkits.mplot3d import Axes3D

#import RIRmeasure_SineSweep
#calType = M.cal_type
#delayType = M.delayType
#fs = M.fs
RIRlen = 1332   # Size of the RIR's Chosen by the previous year's group
#nMics = M.inputChannels       # Mics are our unknown position devices
#nLS = M.outputChannels        # Loudspeakers are our known position devices
#x_bound = M.x_axis    # room bound on the x axis
#y_bound = M.y_axis    # room bound on the y axis
#if calType == 2:
#    z_bound = M.z_axis

#knownPos = M.knownPos # know positions of the Loudspeakers used in the pyroomacoustics simulation

# data contains the RIRs of the simulation it's shape is (nMics*RIRlen , nLS) 
# data = createRir(RIRlen) # Create a RIR with Pyroomacoustics (See RIRsimulation file)

def createDataMatrix(nMics, nLS):
    data = np.zeros((nMics*RIRlen,nLS))
    return data

def fillDataMatrix(data, nMics, nLS):
    lastRecording = np.load('SineSweepMeasures/lastMeasure/RIR.npy')
    for i in np.arange(0,nMics):
        data[i*RIRlen:RIRlen*(i+1),nLS] = lastRecording[0:RIRlen,i]
    return data

# create the bounds (necessary for the scipy minimize function used in calibration)

def createBounds(nMics, x_bound, y_bound, z_bound):
    bounds2D_nodel = np.zeros((nMics*2, 2))
    bounds2D_del = np.zeros((nMics*2 + 1,2))
    bounds3D_nodel = np.zeros((nMics*3,2))
    bounds3D_del = np.zeros((nMics*3 + 1,2))

    for i in range(0,bounds2D_nodel.shape[0]):
        if i%2==0:
            bounds2D_nodel[i,1] = x_bound
            bounds2D_del[i,1] = x_bound
        else:
            bounds2D_nodel[i,1] = y_bound
            bounds2D_del[i,1] = y_bound
    bounds2D_del[-1,1] = 0.5 #Delay bounds in 2D case

    for i in range(0,bounds3D_nodel.shape[0],2):
        bounds3D_nodel[i,1] = x_bound
        bounds3D_del[i,1] = x_bound
    for i in range(1,bounds3D_nodel.shape[0],2):
        bounds3D_nodel[i,1] = y_bound
        bounds3D_del[i,1] = y_bound
    for i in range(2,bounds3D_nodel.shape[0],3):
        bounds3D_nodel[i,1] = z_bound
        bounds3D_del[i,1] = z_bound
    bounds3D_del[-1,1] = 0.5   #Delay bounds in 3D case

    return bounds2D_nodel, bounds2D_del, bounds3D_nodel, bounds3D_del


#Function for finding the direct path of the RIR's (Calibration function)
def find_directPath(this_rir, top_peaks=15):
    this_rir = np.abs(this_rir)     #It computes the absolute value of the RIR to avoid that the first peak is negative
    peaks, _ = find_peaks(this_rir)
    nHighest = (this_rir[peaks]).argsort()[::-1][:top_peaks] # takes the arg of the 15 biggest peaks
    dp = np.sort((peaks[nHighest]))[:1]                      # takes the first (in time) of the 15 biggest peaks
    return dp[0]                                             # dp is the sample the first biggest peak


#Function to compute the distance between two devices through RIR's measurement (Calibration function)
def compute_distance(audio, fs, c, interp_factor = 2, do_interpolation = True):
    distance = np.zeros(shape=(audio.shape[1]))
    for m in range(0,audio.shape[1]):  # audio.shape[1] should be the number of known devices (?)
        if do_interpolation:
            this_rir = audio[:,m]
            sample_ax = np.arange(0, this_rir.shape[0])
            f = interpolate.interp1d(sample_ax, this_rir, kind='quadratic')
            sample_ax_new = np.arange(0, this_rir.shape[0] - 1, 1/interp_factor)
            dp = find_directPath(f(sample_ax_new))
            distance[m] = (dp/interp_factor)*(1/fs) * c

        else:
            this_rir = abs(audio[:,m])
            dp = find_directPath(this_rir)
            distance[m] = dp*(1/fs) * c     # removed 1/interp_factor when not doing interpolation
    return distance

    #Function to estimate the position of the unkown devices in 2D and without delay estimation (Calibration function)
def calibration2D_nodel(data, PosKnown, nUnknown, bnds, fs, c):
    #Initialization of the vector of initial values for the minimization search
    ini = np.zeros(shape=(nUnknown * 2))
    
    #Function that compute the minimization method
    def fun2D_nodel(x1):
        P = np.zeros((nUnknown,data.shape[1]))
        D = np.zeros((nUnknown,data.shape[1]))
        distance = np.zeros((nUnknown,data.shape[1]))
        
        #Computing the distance with the RIR's measurements and filling the matrices
        counter = 0
        for j in range(0,nUnknown):
            distance[j] = compute_distance(data, fs, c)
            for i in range(0, data.shape[1]):
                P[j,i] = (np.sqrt(abs(x1[counter] - PosKnown[i][0])**2 + abs(x1[counter + 1] - PosKnown[i][1])**2))
                D[j,i] = distance[j,i]
            counter = counter + 2

        return sum(sum((P - D )**2))
    
    #Minimization algorithm
    resM = minimize(fun2D_nodel, ini, method='SLSQP', bounds=bnds)
    
    #Printing the results in console log
    counter = 0
    for n in range(0,nUnknown):
            print('Source ',n ,': \n','X: ', resM.x[counter], '[m]', 'Y: ', resM.x[counter + 1], '[m]\n')
            counter = counter + 2
    return resM.x

#Function to estimate the position of the unkown devices in 2D and with delay estimation (Calibration function)
def calibration2D_del(data, PosKnown, nUnknown, bnds, fs, c):
    #Initialization of the vector of initial values for the minimization search
    ini = np.zeros(shape=(nUnknown * 2 + 1))
    
    #Function that compute the minimization method
    def fun2D_del(x1):
        P = np.zeros(shape=(nUnknown,data.shape[1]))
        D = np.zeros(shape=(nUnknown,data.shape[1]))
        T = np.zeros(shape=(nUnknown,data.shape[1]))
        distance = np.zeros(shape=(nUnknown,data.shape[1]))
        
        #Computing the distance with the RIR's measurements and filling the matrices
        counter = 0
        for j in range(0,nUnknown):
            distance[j] = compute_distance(data[j*RIRlen:j*RIRlen + RIRlen - 1,:], fs, c)
            for i in range(0, data.shape[1]):
                P[j,i] = (np.sqrt(abs(x1[counter] - PosKnown[i][0])**2 + abs(x1[counter + 1] - PosKnown[i][1])**2))
                D[j,i] = distance[j,i]
                T[j,i] = x1[nUnknown*2]*c
            counter = counter + 2

        return sum(sum((P - (D - T)) **2))
    
    #Minimization algorithm
    resM = minimize(fun2D_del, ini, method='SLSQP', bounds=bnds)
    
    #Printing the results in console log
    counter = 0
    for n in range(0,nUnknown):
            print('Source ',n ,': \n','X: ', resM.x[counter], '[m]', 'Y: ', resM.x[counter + 1], '[m]\n')
            counter = counter + 2
    print('Delta :',resM.x[nUnknown *2], '[s]')
    return resM.x
    
#Function to estimate the position of the unkown devices in 3D and without delay estimation (Calibration function)
def calibration3D_nodel(audio, fs, PosKnown, c, bnds,nUnknown):
    #Initialization of the vector of initial values for the minimization search
    ini = np.zeros(shape=(nUnknown * 3))
    
    #Function that compute the minimization method
    def fun3D_nodel(x1):
        P = np.zeros(shape=(nUnknown,audio.shape[1]))
        D = np.zeros(shape=(nUnknown,audio.shape[1]))
        distance = np.zeros(shape=(nUnknown,audio.shape[1]))
        
        #Computing the distance with the RIR's measurements and filling the matrices
        counter = 0
        for j in range(0,nUnknown):
            distance[j] = compute_distance(audio[j*RIRlen:j*RIRlen + RIRlen - 1,:], fs, c)
            for i in range(0, audio.shape[1]):
                P[j,i] = (np.sqrt(abs(x1[counter] - PosKnown[i][0])**2 + abs(x1[counter + 1] - PosKnown[i][1])**2 + abs(x1[counter + 2] - PosKnown[i][2])**2))
                D[j,i] = distance[j,i]
            counter = counter + 3

        return sum(sum((P - D) **2))
    
    #Minimization algorithm
    resM = minimize(fun3D_nodel, ini, method='SLSQP', bounds=bnds)
    
    #Printing the results in console log
    counter = 0
    for n in range(0,nUnknown):
            print('Source ',n ,': \n','X: ', resM.x[counter], '[m]', 'Y: ', resM.x[counter + 1], '[m]', 'Z: ', resM.x[counter + 2], '[m]\n')
            counter = counter + 3
    return resM.x      

#Function to estimate the position of the unkown devices in 3D and with delay estimation (Calibration function)
def calibration3D_del(audio, fs, PosKnown, c, bnds,nUnknown):
    #Initialization of the vector of initial values for the minimization search
    ini = np.zeros(shape=(nUnknown * 3 + 1))
    
    #Function that compute the minimization method
    def fun3D_del(x1):
        #Initializing the matrix with zeroes
        P = np.zeros(shape=(nUnknown,audio.shape[1]))
        D = np.zeros(shape=(nUnknown,audio.shape[1]))
        T = np.zeros(shape=(nUnknown,audio.shape[1]))
        distance = np.zeros(shape=(nUnknown,audio.shape[1]))
        
        #Computing the distance with the RIR's measurements and filling the matrices
        counter = 0
        for j in range(0,nUnknown):
            distance[j] = compute_distance(audio[j*RIRlen:j*RIRlen + RIRlen - 1,:], fs, c)
            for i in range(0, audio.shape[1]):
                P[j,i] = (np.sqrt(abs(x1[counter] - PosKnown[i][0])**2 + abs(x1[counter + 1] - PosKnown[i][1])**2 + abs(x1[counter + 2] - PosKnown[i][2])**2))
                D[j,i] = distance[j,i]
                T[j,i] = x1[nUnknown*3]*c
            counter = counter + 3
            
        return sum(sum((P - (D - T)) **2))
    
    #Minimization algorithm
    resM = minimize(fun3D_del, ini, method='SLSQP', bounds=bnds)
    
    #Printing the results in console log
    counter = 0
    for n in range(0,nUnknown):
            print('Source ',n ,': \n','X: ', resM.x[counter], '[m]', 'Y: ', resM.x[counter + 1], '[m]', 'Z: ', resM.x[counter + 2], '[m]\n')
            counter = counter + 3
    print('Delta :',resM.x[nUnknown *3], '[s]')
    return resM.x

#Function to compute the estimation position in 2D/3D and with/without estimation delay (GUI function)
def calculate_Calibration(data, nMics, nLS, calType, delayType, measureMethod, c, fs, knownPos, x_bound, y_bound, z_bound):
    #Number of unknown positions
    upd = int(nMics)
    #Arrays of zeroes for the plots
    x = np.zeros(shape=(upd))
    y = np.zeros(shape=(upd))
    z = np.zeros(shape=(upd))
    
    bounds2D_nodel, bounds2D_del, bounds3D_nodel, bounds3D_del = createBounds(nMics, x_bound, y_bound, z_bound)
    #data = createDataMatrix(nMics, nLS)

    #If we are in a 3D case with estimation delay:
    if (calType == 2 and delayType == 1):
        #Postion estimation
        pos_3Ddel = calibration3D_del(data,fs = fs, PosKnown = knownPos ,c = c,bnds = bounds3D_del,nUnknown = nMics)
        
        #Filling the plot vectors with their correspondent coordinates and plotting the result
        counter1 = 0
        for n in range(0,upd):
            x[n] = pos_3Ddel[counter1]
            y[n] = pos_3Ddel[counter1 + 1]
            z[n] = pos_3Ddel[counter1 + 2]
            counter1 = counter1 + 3
            
        fig = plt.figure(figsize=(4,4))
        ax = Axes3D(fig, auto_add_to_figure=False)
        ax.scatter(x,y,z, marker = 'o')
        ax.grid()
        ax.legend(['With delay'])
        ax.set_xlabel('$x[m]$', fontsize=18)
        ax.set_ylabel('$y[m]$', fontsize=18)
        ax.set_zlabel('$z[m]$', fontsize=18)
        fig.add_axes(ax)
        plt.show()
    
    #If we are in a 3D case without estimation delay:
    if (calType == 2 and delayType == 2):
        #Postion estimation
        pos_3Dnodel = calibration3D_nodel(data,fs = fs, PosKnown = knownPos ,c = c,bnds = bounds3D_nodel,nUnknown = nMics)
        
        #Filling the plot vectors with their correspondent coordinates and plotting the result
        counter1 = 0
        for n in range(0,upd):
            x[n] = pos_3Dnodel[counter1]
            y[n] = pos_3Dnodel[counter1 + 1]
            z[n] = pos_3Dnodel[counter1 + 2]
            counter1 = counter1 + 3
        
        fig = plt.figure(figsize=(4,4))
        ax = Axes3D(fig, auto_add_to_figure=False)
        ax.scatter(x,y,z, marker = 'o')
        ax.grid()
        ax.legend(['No delay'])
        ax.set_xlabel('$x[m]$', fontsize=18)
        ax.set_ylabel('$y[m]$', fontsize=18)
        ax.set_zlabel('$z[m]$', fontsize=18)
        fig.add_axes(ax)
        plt.show()

    #If we are in a 2D case with estimation delay:
    if (calType == 1 and delayType == 1):
        #Postion estimation
        pos_2Ddel = calibration2D_del(data ,fs = fs, PosKnown = knownPos ,c = c,bnds = bounds2D_del,nUnknown = nMics)
        
        #Filling the plot vectors with their correspondent coordinates and plotting the result
        counter1 = 0
        for n in range(0,upd):
            x[n] = pos_2Ddel[counter1]
            y[n] = pos_2Ddel[counter1 + 1]
            counter1 = counter1 + 2
            
        fig = plt.figure(figsize=(4,4))
        plt.scatter(x, y, marker = 'o')
        plt.title("Estimated position plane xy")
        plt.grid()
        plt.xlabel('x[m]')
        plt.ylabel('y[m]')
        plt.legend(['With delay'])
        plt.show()
        #plt.xlim((0,x_bound))
        #plt.ylim((0,y_bound))
        
    #If we are in a 2D case without estimation delay:   
    if (calType == 1 and delayType == 2):
        #Postion estimation
        pos_2Dnodel = calibration2D_nodel(data,fs = fs, PosKnown = knownPos ,c = c,bnds = bounds2D_nodel,nUnknown = nMics)
        
        #Filling the plot vectors with their correspondent coordinates and plotting the result
        counter1 = 0
        for n in range(0,upd):
            x[n] = pos_2Dnodel[counter1]
            y[n] = pos_2Dnodel[counter1 + 1]
            counter1 = counter1 + 2
            
        fig = plt.figure(figsize=(4,4))
        plt.scatter(x, y, marker = 'o')
        plt.title("Estimated position plane xy")
        plt.grid()
        plt.xlabel('x[m]')
        plt.ylabel('y[m]')
        plt.legend(['No delay'])
        plt.show()

    if measureMethod == 1:
        fig.savefig('SineSweepMeasures/calibrationGraph.png', bbox_inches='tight')
    else:
        fig.savefig('MLSMeasures/calibrationGraph.png')