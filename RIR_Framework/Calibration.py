import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import minimize
from scipy import interpolate
from RIRsimulation import createRir

RIRlen = 1332   # Size of the RIR's Chosen by the previous year's group
nMics = 1       # Mics are our unknown position devices
nLS = 3         # Loudspeakers are our known position devices
x_bound = 10    # room bound on the x axis
y_bound = 10    # room bound on the y axis
z_bound = 4

knownPos = [[4,4,1.5],[5,8,1.5],[8,6,1.5],[2., 2., 1.5]] # know positions of the Loudspeakers used in the pyroomacoustics simulation

# data contains the RIRs of the simulation it's shape is (nMics*RIRlen , nLS) 
data = createRir(RIRlen) # Create a RIR with Pyroomacoustics (See RIRsimulation file)

# create the bounds (necessary for the scipy minimize function used in calibration)
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


#Function for finding the direct path of the RIR's (Calibration function)
def find_directPath(this_rir, top_peaks=15):
    this_rir = np.abs(this_rir)     #It computes the absolute value of the RIR to avoid that the first peak is negative
    peaks, _ = find_peaks(this_rir)
    nHighest = (this_rir[peaks]).argsort()[::-1][:top_peaks] # takes the arg of the 15 biggest peaks
    dp = np.sort((peaks[nHighest]))[:1]                      # takes the first (in time) of the 15 biggest peaks
    return dp[0]                                                # dp is the sample the first biggest peak


#Function to compute the distance between two devices through RIR's measurement (Calibration function)
def compute_distance(audio,fs=44100,c=343,interp_factor = 2, do_interpolation = True):
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
def calibration2D_nodel(data, PosKnown, nUnknown, bnds, fs=44100, c=343):
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
def calibration2D_del(data, PosKnown, nUnknown, bnds, fs=44100, c=343):
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
                D[j,i] = distance[j,i];
            counter = counter + 3

        return sum(sum((P - D) **2));
    
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
        T = np.zeros(shape=(nUnknown,audio.shape[1]));
        distance = np.zeros(shape=(nUnknown,audio.shape[1]))
        
        #Computing the distance with the RIR's measurements and filling the matrices
        counter = 0
        for j in range(0,nUnknown):
            distance[j] = compute_distance(audio[j*RIRlen:j*RIRlen + RIRlen - 1,:], fs, c)
            for i in range(0, audio.shape[1]):
                P[j,i] = (np.sqrt(abs(x1[counter] - PosKnown[i][0])**2 + abs(x1[counter + 1] - PosKnown[i][1])**2 + abs(x1[counter + 2] - PosKnown[i][2])**2))
                D[j,i] = distance[j,i];
                T[j,i] = x1[nUnknown*3]*c
            counter = counter + 3
            
        return sum(sum((P - (D - T)) **2));
    
    #Minimization algorithm
    resM = minimize(fun3D_del, ini, method='SLSQP', bounds=bnds)
    
    #Printing the results in console log
    counter = 0
    for n in range(0,nUnknown):
            print('Source ',n ,': \n','X: ', resM.x[counter], '[m]', 'Y: ', resM.x[counter + 1], '[m]', 'Z: ', resM.x[counter + 2], '[m]\n')
            counter = counter + 3
    print('Delta :',resM.x[nUnknown *3], '[s]')
    return resM.x

#RIR = np.load('Sine_Sweep_Recordings/lastRecording/RIR.npy')
