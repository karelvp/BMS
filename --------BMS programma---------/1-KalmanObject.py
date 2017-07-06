import math as m
import sympy as sp
import numpy as np
from scipy.misc import derivative
import parameterbepaling as pb
import matplotlib.pyplot as plt

"""

Libraries:

Sympy --> differentiation of OCV symbolicly
math  --> general mathematics
numpy --> apply matrices and matrix calculation


WAT MOET ER GEBEUREN bij read?

een object voor initialisatie

een object voor als het continue loopt

een object voor een window van errors op te zetten met vaste covariantiematrices


"""


#---------------------------------KALMANOBJECT----------------------------------


def getKalmanStart(Voltage1, Voltage2, Voltage3, VoltageM, Current, T, sampletime):
    """
        Initialisation of Kalman filter
        
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

    selfdisch = 35.0/(360.0*24.0)   #this is the %SOC per day that gets lost due to selfdischarge comes from datasheet

    Ownusg = 0.01                   #this is still unknown


    """ from here the objects differ from eachother """
    

    #----------------------------initialisation-------------------------

    Upk = 0.0
    SOC =0.5

    sigmaSOC = 0.8*(10**-3) #estimate of standard deviation of SOC
    sigmaUpk = 1*(10**-5)   #estimate of standard deviation of Upk

    sigmaUt = 0.001         #standard deviatian of Terminal voltage measurement


    P0 = np.matrix([sigmaSOC**2, sigmaSOC*sigmaUpk],[sigmaSOC*sigmaUpk,sigmaUpk**2])    #initial error covariance

    covQ = np.matrix([sigmaSOC**2, 0.0],[0.0 ,sigmaUpk**2])                             #initial process noise covariance
    covR = np.matrix([sigmaUt])                                                         #initial measurement noise covariance

    #----------------------------Variables of State-Space model----------

    prev_State_poster = np.matrix([[Upk],[SOC]])    #previous state after measurement update
    next_State_prior = np.matrix([0])               #next state prior to measurement update; empty matrix but helps to understand structure of programm
    next_State_poster = np.matrix([0])              #next state poster to measurement update; empty matrix but helps to understand structure of programm

    Output = np.matrix([Voltage1])

    Input = np.matrix([Current+selfdisch+Ownusg])   #Extra input in model than just the current
    
    #------------------State space matrices-----------------------------


    

    A0 = np.matrix([[m.exp(-sampletime/(Rp(prev_State_poster[1,0])*Cp(prev_State_poster[1,0]))), 0.0], [0.0, 1.0]]) 

    B0 = np.matrix([[Rp*(1-m.exp(-sampletime/(Rp(prev_State_poster[1,0])*Cp(prev_State_poster[1,0]))))], [ Eff*sampletime/(3600.0*Capacity)]]) 

    C0 = np.matrix([[1.0, dOCVdSOC(prev_State_poster[1,0])]]) #niet zeker van dit

    D0 = np.matrix([[R0(prev_State_poster[1,0])]])


    """ KALMAN LOOP --> (1) (2) (3) (4) (5) are the main equations"""
    
    #------------TIME UPDATE -----------------------------------------

    next_State_prior = A0 * prev_State_poster + B0 * Input      #(1) state space update/ prediction

    Pk_prior = (A0 * Pk0 * (A0.transpose())) + covQ             #(2) error covariance update


    #------------MEASUREMENT UPDATE ----------------------------------

    aux = (C0 * Pk_prior * (C0.transpose())) + covR; aux        #auxiliary matrix
    inv_aux = aux.getI()                                        #inverse of auxiliary matrix
        
    Hk = Pk_prior * (C0.transpose()) * inv_aux                  #(3)Kalman gain

    error = Output - C0 * next_State_prior - D0 * Input         #remaining error 

    """ Moet er bij error nog extra ocv(SOC) afgetrokken worden? """

    next_State_poster = next_State_prior + Hk * error           #(4) measurement update

    I = np.eye(2, dtype='double')                               #identity matrix

    Pk_poster = (I - Hk*C0)*Pk_prior                            #(5)error covariance update

    
    #--------------Return--------------------------------------------
    
    List = []
    List.append(next_State_poster)
    List.append(Pk_poster)
    List.append(error)

    return List





def getKalman1(List, Voltage1, Voltage2, Voltage3, VoltageM, Current, T, sampletime):
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

    
    #--------------Return--------------------------------------------
    
    List = []
    List.append(next_State_poster)
    List.append(next_P_poster)
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

