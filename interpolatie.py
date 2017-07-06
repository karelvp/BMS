import math

def getIntSOCValue(SOC2, SOC1, SOCx, R2, R1):
    rico = (R2 - R1) / (SOC2 - SOC1)
    Rx = R1 + rico * (SOCx - SOC1)
    return Rx

def getIntCurrentValue(I2, I1, Ix, R2, R1):
    rico = (R2 - R1) / (I2 - I1)
    Rx = R1 + rico * (Ix - I1)
    return Rx 

def getIntTemperatureValue(T2, T1, Tx, R2, R1):
    rico = (R2 - R1) / (T2 - T1)
    Rx = R1 + rico * (Tx - T1)
    return Rx 
    



