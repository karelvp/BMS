import math
import time as tm
import numpy as np
import xlrd



def getSOC (SOC1, SOC2, I_b, sampletime, Total_capacity, Eff):
    '''values without underscore are the k1'th (Ib) and values with underscore are the k+1'th (I_b) sample value'''
    SOC2 = SOC1 + (sampletime/Total_capacity)*Eff*I_b
    return SOC2


def getCoulombicEff()
    ''' kijk naar pc voor artikel'''
    return Eff





def calculateVres(SOC1, SOC2, Ib, I_b, I1, I2, I3, sampletime, T2, T1):
    '''values without underscore are the k1'th (Ib) and values with underscore are the k+1'th (I_b) sample value'''
    #read in excell
    R0 

    R0v
    
    R1
    C1

    R2
    C2

    R3
    C3
    
    meanIb = (Ib + I_b)/2

    I_1 = math.exp(-sampletime/(R1*C1))*I1 + (1-math.exp(-sampletime/(R1*C1)))*meanIb
    
    I_2 = math.exp(-sampletime/(R2*C2))*I2 + (1-math.exp(-sampletime/(R2*C2)))*meanIb

    I_3 = math.exp(-sampletime/(R3*C3))*I3 + (1-math.exp(-sampletime/(R3*C3)))*meanIb

    Vr = I_b*R0v + I_b*R0 + I_1*R1 + I_2*R2 + I_3*R3

    return Vr;




