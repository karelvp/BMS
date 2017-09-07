import math

import math as m

import numpy as np
from numpy.linalg import inv

import parameterbepaling as pb
import xlrd

import interpolatie as itp

"""

programma met objecten voor extended kalman filter

Libraries:

math  --> general mathematics
numpy --> apply matrices and matrix calculation
parameterbepaling --> lookuptables

de ingelezen file parameterwaarden bevat alle LUT's voor het statespace model

"""


#-------------------------READ-IN----------------------------------------

file_location = r"C:\Users\parameterwaarden.xlsx"
workbook = xlrd.open_workbook(file_location)

R0dischtable = workbook.sheet_by_index(0)
R0chtable = workbook.sheet_by_index(1)
R1chtable = workbook.sheet_by_index(2)
R1dischtable = workbook.sheet_by_index(3)
C1dischtable = workbook.sheet_by_index(4)
C1chtable = workbook.sheet_by_index(5)

C2table = workbook.sheet_by_index(6)
R2table = workbook.sheet_by_index(7)
C3table = workbook.sheet_by_index(8)
R3table = workbook.sheet_by_index(9)

OCVtable = workbook.sheet_by_index(10) 
maxdevtable = workbook.sheet_by_index(11)
derivtable = workbook.sheet_by_index(12)


#---------------------------------KALMANOBJECT----------------------------------


def getKalmanStart(Voltage, Current, T, sampletime):
    """
        Initialisation of Kalman filter
        
    """

    
    #----------------------------Capacity--------------------------------

    Capacity = 132.5


    Eff = 0.9986 #efficiency of charging and discharging

  
    #----------------------------initialisation-------------------------


    Up1=    0.0
    Up2=    0.0
    Up3=    0.0
    SOC=   0.5
    Vh=    -0.004

    sigmaSOC = 0.1 #estimate of standard deviation of SOC
    sigmaUpk = 0.00 #estimate of standard deviation of Upk
    sigmaVh = 0.000

    sigmaUt = 0.001         #standard deviatian of Terminal voltage measurement


    P0 = np.matrix([[4.8e-8, -3.3e-11, -1.44e-10, 1.28e-08, -9.6e-14],[-3.3e-11,4.09e-7, -7.18e-9, -3.4e-7, -8.0e-13],[-1.44e-10,-7.18e-9,1.67e-5, -1.599e-5, -3.32e-12],[-1.28e-8,-3.406e-7,-1.599e-6,4e-2,-4.2e-10],[-9.6e-14,-8.0e-13,-3.32e-12,-4.2e-10,9.9e-9]])    #initial error covariance

    covQ = np.matrix([[sigmaUpk**2, 0, 0, 0, 0],[0,sigmaUpk**2, 0, 0, 0],[0,0, sigmaUpk**2, 0, 0],[0,0,0,sigmaSOC**2,0],[0,0,0,0,sigmaVh**2]])                            #initial process noise covariance
    covR = np.matrix([sigmaUt])                                                         #initial measurement noise covariance

    #----------------------------Variables of State-Space model----------

    prev_State_poster = np.matrix([[Up1],[Up2],[Up3],[SOC],[Vh]])    #previous state after measurement update
    next_State_prior = np.matrix([0])               #next state prior to measurement update; empty matrix but helps to understand structure of programm
    next_State_poster = np.matrix([0])              #next state poster to measurement update; empty matrix but helps to understand structure of programm

    Output = np.matrix([Voltage])

    if (Current > 0.0):
        Md = pb.getVal3(prev_State_poster.item((3,0)),25.0,maxdevtable)
    else:
        Md = -1.0* pb.getVal3(prev_State_poster.item((3,0)),25.0,maxdevtable)

    Input = np.matrix([[Current],[Md]])   #Extra input in model than just the current


    #----------------------------Parameters--------------------------------

    
    if (Current > 0.0): # choose charging
    
        if (abs(Current) > 30.0): 
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,Current,25.0,R0chtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,Current,25.0,R1chtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,Current,25.0,C1chtable)
        else: 
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R0chtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R1chtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,C1chtable)

    else:               #choose discharging
        if (abs(Current) > 30.0): 
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R0dischtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R1dischtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,C1dischtable)

        else:
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R0dischtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R1dischtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,C1dischtable)


    R2 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,R2table)
    C2 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,C2table)
    R3 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,R3table)
    C3 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,C3table)


    deriv = pb.getVal3(prev_State_poster.item((3,0))*100.0,25.0,derivtable)
    OCV = pb.getVal3(prev_State_poster.item((3,0))*100.0,25.0,OCVtable)

 

    Ch = 1.0
    Rh = abs(Current)*20.0/(3600.0*132.5)
  
    #------------------State space matrices-----------------------------


    if (abs(Current) <1.0):

        A0 =np.matrix([[math.exp((-sampletime)/(R1*C1)), 0.0 , 0.0 , 0.0 , 0.0], [0.0, math.exp((-sampletime)/(R2*C2)) , 0.0 , 0.0 , 0.0],[0.0, 0.0 , math.exp((-sampletime)/(R3*C3)) , 0.0 , 0.0],[0.0, 0.0 , 0.0 , 1.0 , 0.0],[0.0, 0.0 , 0.0 , 0.0 , 0.0]]) 

        B0 =np.matrix([[R1*(1-m.exp(-sampletime/(R1*C1))),0.0], [R2*(1-m.exp(-sampletime/(R2*C2))),0.0],[R3*(1-m.exp(-sampletime/(R3*C3))),0.0],[0.0, Eff*sampletime/(3600.0*Capacity)],[0.0,1.0]]) 
    else:

        A0 =np.matrix([[math.exp((sampletime)/(R1*C1)), 0.0 , 0.0 , 0.0 , 0.0], [0.0, math.exp((sampletime)/(R2*C2)) , 0.0 , 0.0 , 0.0],[0.0, 0.0 , math.exp((sampletime)/(R3*C3)) , 0.0 , 0.0],[0.0, 0.0 , 0.0 , 1.0 , 0.0],[0.0, 0.0 , 0.0 , 0.0 , math.exp((sampletime)/(Rh*Ch))]]) 

        B0 =np.matrix([[R1*(1-m.exp(-sampletime/(R1*C1))),0.0], [R2*(1-m.exp(-sampletime/(R2*C2))),0.0],[R3*(1-m.exp(-sampletime/(R3*C3))),0.0],[0.0, Eff*sampletime/(3600.0*Capacity)],[0.0,(1-m.exp(-sampletime/(Rh*Ch)))]]) 

    
    
    C0 =np.matrix([[float(1.0) ,float(1.0),float(1.0), float(deriv), float(1.0)]])

    C0T =np.matrix([[float(1.0)],[float(1.0)],[float(1.0)], [float(deriv)], [float(1.0)]])

    D0 =np.matrix([[R0,0]])


    """ KALMAN LOOP --> (1) (2) (3) (4) (5) are the main equations"""
    
    #------------TIME UPDATE -----------------------------------------

    next_State_prior = A0 * prev_State_poster + B0 * Input      #(1) state space update/ prediction

    Pk_prior = (A0 * P0 * (A0.transpose())) + covQ              #(2) error covariance update

    

    #------------MEASUREMENT UPDATE ----------------------------------

    
   
    

    aux = C0*Pk_prior*C0T + covR          #auxiliary matrix
    
    invaux = inv(aux)                                       #inverse of auxiliary matrix
        
    Hk = Pk_prior * (C0.transpose()) * invaux                  #(3)Kalman gain

   

    error = Output - C0 * next_State_prior + C0.item((0,3))*next_State_prior.item((3,0)) - OCV - D0 * Input         #remaining error 

  
    
    """ Moet er bij error nog extra ocv(SOC) afgetrokken worden? """

    next_State_poster = next_State_prior + Hk * error           #(4) measurement update

  

    I = np.eye(5, dtype='double')                               #identity matrix

    Pk_poster = (I - Hk*C0)*Pk_prior                            #(5)error covariance update

    
    #--------------Return--------------------------------------------
    
    List = []
    List.append(next_State_poster)
    List.append(Pk_poster)
    List.append(error)

    return List





def getKalman1(List, Voltage, Current, T, sampletime):
    """

        In list : [ xprev, pkposter , error]
        The difference between Kalmanstart en kalman1 is that P0 and X0 aren't used but the data from the previous estimate.

    """


    
    #----------------------------Capacity--------------------------------

    Capacity = 132.5


    Eff = 0.9986 #efficiency of charging and discharging

    #----------------------------Get previous state-------------------------


    sigmaSOC = 0.01 #estimate of standard deviation of SOC
    sigmaUpk = 0.0 #estimate of standard deviation of Upk
    sigmaVh = 0.0 #estimate of standard deviation of HysteresisVoltage

    sigmaUt = 0.005         #standard deviatian of Terminal voltage measurement
    
    Pprev = List[1]

    covQ = np.matrix([[sigmaUpk**2, 0, 0, 0, 0],[0,sigmaUpk**2, 0, 0, 0],[0,0, sigmaUpk**2, 0, 0],[0,0,0,sigmaSOC**2,0],[0,0,0,0,sigmaVh**2]])                            #initial process noise covariance
    covR = np.matrix([sigmaUt])
    
    #----------------------------Variables of State-Space model----------

    prev_State_poster = List[0]    #previous state after measurement update
    next_State_prior = np.matrix([0])               #next state prior to measurement update; empty matrix but helps to understand structure of programm
    next_State_poster = np.matrix([0])              #next state poster to measurement update; empty matrix but helps to understand structure of programm

    Output = np.matrix([Voltage])

    if (Current > 0.0):
        Md = pb.getVal3(prev_State_poster.item((3,0)),25.0,maxdevtable)
    else:
        Md = -1.0* pb.getVal3(prev_State_poster.item((3,0)),25.0,maxdevtable)

    Input = np.matrix([[Current],[Md]])   #Extra input in model than just the current
    
    #----------------------------Parameters--------------------------------

    
    if (Current > 0.0): # choose charging
    
        if (abs(Current) > 30.0): 
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,Current,25.0,R0chtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,Current,25.0,R1chtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,Current,25.0,C1chtable)
        else: 
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R0chtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R1chtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,C1chtable)

    else:               #choose discharging
        if (abs(Current) > 30.0): 
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R0dischtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R1dischtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,C1dischtable)

        else:
            R0 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R0dischtable)
            R1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,R1dischtable)
            C1 = pb.getVal(prev_State_poster.item((3,0))*100.0,50.0,25.0,C1dischtable)


    R2 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,R2table)
    C2 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,C2table)
    R3 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,R3table)
    C3 = pb.getVal2(prev_State_poster.item((3,0))*100.0,25.0,C3table)


    deriv = pb.getVal3(prev_State_poster.item((3,0))*100.0,25.0,derivtable)
    OCV = pb.getVal3(prev_State_poster.item((3,0))*100.0,25.0,OCVtable)

 

    Ch = 1.0
    Rh = abs(Current)*20.0/(3600.0*132.5)

    #---------------------------self-discharge and own usage--------------

    """
        Selfdischarge and own usage will be set into the model via an extra current increase of the individual cells.

    """

    selfdisch = 35.0/(360.0*24.0) #this is the %SOC per day that gets lost due to selfdischarge comes from datasheet

    Ownusg = 0.01 #this is still unknown


    """ from here the objects differ from eachother """
    

    #------------------State space matrices-----------------------------


    if (abs(Current) <1.0):

        A0 =np.matrix([[math.exp((-sampletime)/(R1*C1)), 0.0 , 0.0 , 0.0 , 0.0], [0.0, math.exp((-sampletime)/(R2*C2)) , 0.0 , 0.0 , 0.0],[0.0, 0.0 , math.exp((-sampletime)/(R3*C3)) , 0.0 , 0.0],[0.0, 0.0 , 0.0 , 1.0 , 0.0],[0.0, 0.0 , 0.0 , 0.0 , 0.0]]) 

        B0 =np.matrix([[R1*(1-m.exp(-sampletime/(R1*C1))),0.0], [R2*(1-m.exp(-sampletime/(R2*C2))),0.0],[R3*(1-m.exp(-sampletime/(R3*C3))),0.0],[0.0, Eff*sampletime/(3600.0*Capacity)],[0.0,1.0]]) 
    else:

        A0 =np.matrix([[math.exp((-sampletime)/(R1*C1)), 0.0 , 0.0 , 0.0 , 0.0], [0.0, math.exp((-sampletime)/(R2*C2)) , 0.0 , 0.0 , 0.0],[0.0, 0.0 , math.exp((-sampletime)/(R3*C3)) , 0.0 , 0.0],[0.0, 0.0 , 0.0 , 1.0 , 0.0],[0.0, 0.0 , 0.0 , 0.0 , math.exp((-sampletime)/(Rh*Ch))]]) 

        B0 =np.matrix([[R1*(1-m.exp(-sampletime/(R1*C1))),0.0], [R2*(1-m.exp(-sampletime/(R2*C2))),0.0],[R3*(1-m.exp(-sampletime/(R3*C3))),0.0],[0.0, Eff*sampletime/(3600.0*Capacity)],[0.0,(1-m.exp(-sampletime/(Rh*Ch)))]]) 

    
    
    C0 =np.matrix([[float(1.0) ,float(1.0),float(1.0), float(deriv), float(1.0)]])

    C0T =np.matrix([[float(1.0)],[float(1.0)],[float(1.0)], [float(deriv)], [float(1.0)]])

    D0 =np.matrix([[R0,0]])

    """ KALMAN LOOP --> (1) (2) (3) (4) (5) are the main equations"""
    
    #------------TIME UPDATE -----------------------------------------

    next_State_prior = A0 * prev_State_poster + B0 * Input      #(1) state space update/ prediction

    Pk_prior = (A0 * Pprev * (A0.transpose())) + covQ              #(2) error covariance update

   

    #------------MEASUREMENT UPDATE ----------------------------------

    aux = C0*Pk_prior*C0T + covR          #auxiliary matrix
    
    invaux = inv(aux)                                       #inverse of auxiliary matrix
        
    Hk = Pk_prior * (C0.transpose()) * invaux                  #(3)Kalman gain

   

    error = Output - C0 * next_State_prior + C0.item((0,3))*next_State_prior.item((3,0)) - OCV - D0 * Input         #remaining error 

   
    
    """ Moet er bij error nog extra ocv(SOC) afgetrokken worden? """

    next_State_poster = next_State_prior + Hk * error           #(4) measurement update

    if ( next_State_poster.item(3,0) < 0.007):
        next_State_poster[3,0] = 0.007
    if ( next_State_poster.item(3,0) > 0.86):
        next_State_poster[3,0] = 0.86
    
    I = np.eye(5, dtype='double')                               #identity matrix

    Pk_poster = (I - Hk*C0)*Pk_prior                            #(5)error covariance update

    
    #--------------Return--------------------------------------------
    
    List = []
    List.append(next_State_poster)
    List.append(Pk_poster)
    List.append(error)

    return List



def getKalman2(List, Errorlist, Voltage1, Voltage2, Voltage3, VoltageM, Current, T, sampletime):    #list now contains just State and error covariance. Errors are in another list
    """
        Recursive updating of covariance matrices R and Q can't be executed
        because the window doesn't have the correct size.

        The difference between Kalmanstart en kalman1 is that P0 and X0 aren't used but the data from the previous estimate.

    """


    
    #----------------------------Capacity--------------------------------

    Capacity = 100.0

    Qi = 1.0 #influence of Current on Capacity
    Qt = 1.0 #influence of Temperature on Capacity

    Eff = 1.0 #efficiency of charging and discharging

    #----------------------------Parameters--------------------------------
    z = sp.Symbol('z')  #symbolic for SOC

    #Rp = pb.getRp(SOC,I,T)
    #Cp = pb.getRp(SOC,I,T)
    #R0 = pb.getRp(SOC,I,T)

    def R0(z):
        return -1.6693*(10**-6)*(z**3)+3.3387*(10**-5)*(z**2)-2.0059*(10**-4)*z+0.0017911

    def Cp(z):
        return 3.0612*(10**4)

    def Rp(z):
        return 0.00331

    

    #----------------------------Open Circuit Voltage-----------------------

    def OCV(z):                 #polynomial fit isn't correct
        p1 =    0.008455  
        p2 =     -0.1075  
        p3 =    -0.05198  
        p4 =      0.3857  
        p5 =     0.07347  
        p6 =      -0.398  
        p7 =    -0.03754  
        p8 =     0.06001  
        p9 =       3.294

        return p1*z**8 + p2*z**7 + p3*z**6 + p4*z**5 + p5*z**4 + p6*z**3 + p7*z**2 + p8*z + p9

    dOCVdSOC = sp.diff(OCV, z)

    def dOCVdSOC(z):
        return derivative(OCV,z)



    #---------------------------self-discharge and own usage--------------

    """
        Selfdischarge and own usage will be set into the model via an extra current increase of the individual cells.

    """

    selfdisch = 35.0/(360.0*24.0) #this is the %SOC per day that gets lost due to selfdischarge comes from datasheet

    Ownusg = 0.01 #this is still unknown


    """ from here the objects differ from eachother """
    

    #---------------noise covariances and error covariance------------------


    sigmaSOC = 0.8*(10**-3) #estimate of standard deviation of SOC
    sigmaUpk = 1*(10**-5)   #estimate of standard deviation of Upk

    sigmaUt = 0.001         #standard deviatian of Terminal voltage measurement


    prev_P_poster = List[1]
    next_P_prior = np.matrix([0])
    next_P_poster = np.matrix([0])
    

    covQ = np.matrix([sigmaSOC**2, 0.0],[0.0 ,sigmaUpk**2])                             #initial process noise covariance
    covR = np.matrix([sigmaUt])                                                         #initial measurement noise covariance

    #----------------------------Variables of State-Space model----------

    prev_State_poster = List[0]                     #previous state after measurement update
    next_State_prior = np.matrix([0])               #next state prior to measurement update; empty matrix but helps to understand structure of programm
    next_State_poster = np.matrix([0])              #next state poster to measurement update; empty matrix but helps to understand structure of programm
    
    Output = np.matrix([Voltage1])

    Input = np.matrix([Current+selfdisch+Ownusg])   #Extra input in model than just the current
    
    #------------------State space matrices-----------------------------


    Ak = np.matrix([[m.exp(-sampletime/(Rp(prev_State_poster[1,0])*Cp(prev_State_poster[1,0]))), 0.0], [0.0, 1.0]]) 

    Bk = np.matrix([[Rp*(1-m.exp(-sampletime/(Rp(prev_State_poster[1,0])*Cp(prev_State_poster[1,0]))))], [ Eff*sampletime/(3600.0*Capacity)]]) 

    Ck = np.matrix([[1.0, dOCVdSOC(prev_State_poster[1,0])]]) #niet zeker van dit

    Dk = np.matrix([[R0(prev_State_poster[1,0])]])


    """ Kalman loop --> (1) (2) (3) (4) (5) are the main equations"""
    
    #------------TIME UPDATE -----------------------------------------

    next_State_prior = Ak * prev_State_poster + Bk * Input              #(1) state space update/ prediction

    next_P_prior = (Ak * prev_P_poster * (Ak.transpose())) + covQ       #(2) error covariance update


    #------------MEASUREMENT UPDATE ----------------------------------

    aux = (Ck * next_P_prior * (Ck.transpose())) + covR; aux            #auxiliary matrix
    inv_aux = aux.getI()                                                #inverse of auxiliary matrix
        
    Hk = next_P_prior * (Ck.transpose()) * inv_aux                      #(3)Kalman gain

    error = Output - Ck * next_State_prior - Dk * Input                 #remaining error 

    """ Moet er bij error nog extra ocv(SOC) afgetrokken worden? """

    next_State_poster = next_State_prior + Hk * error                   #(4) measurement update

    I = np.eye(2, dtype='double')                                       #identity matrix

    next_P_poster = (I - Hk * Ck)* next_P_prior                         #(5)error covariance update


    #----------ADAPTIVE Rk and Qk estimation ------------------------








    
    #--------------Return--------------------------------------------
    
    List = []
    List.append(next_State_poster)
    List.append(next_P_poster)
    List.append(error)

    return List

