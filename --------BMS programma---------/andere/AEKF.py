#----------------------------IMPORT------------------------------------

import math
import csv
import time as tm
import numpy as np

import parameterbepaling as pb

"""

WAT MOET ER GEBEUREN bij initial read?

een object voor als het continue draait


"""



#-------------------------InitialREAD--------------------------------

VoltageSlave1 = lib.readinVoltagecell(1)  "this object is yet to be made"
VoltageSlave2 = lib.readinVoltagecell(2)  "this object is yet to be made"
VoltageSlave3 = lib.readinVoltagecell(3)  "this object is yet to be made"
VoltageMaster = lib.readinVoltagecell(4)  "this object is yet to be made"

Current = lib.readinCurrent()             "this object is yet to be made"

T = lib.readinTemperature()               "this object is yet to be made"




#----------------------------VARIABLES--------------------------------


Capacity = 100.0

Rp = pb.getRp(SOC,I,T)
Cp = pb.getRp(SOC,I,T)
R0 = pb.getRp(SOC,I,T)

sampletime = 1.0 #needs to be changed


OCV = 3.0*SOC4 + SOC^3 + SOC^2 + SOC + 3.0

dOCVdSOC = 12 #zelf afleiden moet nog gebeuren


#---------------------------------------------------------------------







''' Set initial value for matrix X0 and P0 '''


#---------------------------------------------------
SOC1 = 0.5 #set value
Upk = 1.96 #get this value out of main programm

sigmaSOC = 0.02 #estimate of sqrt(variance) of SOC
sigmaUpk = 0.02 #estimate of sqrt(variance) of Upk


X0 = np.matrix([[Upk],[SOC1]])
P0 = np.matrix([sigmaSOC**2,0],[0,sigmaUpk]])

#---------------------------------------------------




Ak = np.matrix([[math.exp(-sampletime/(Rp*Cp)), 0], [0, 1]]) 

Bk = np.matrix([[Rp*(1-math.exp(-sampletime/(Rp*Cp)))], [ sampletime/(3600*Capacity)]]) 

Ck = np.matrix([[1], [dOCVdSOC]])

Dk = np.matrix([[R0]])





'''
There is data at the k'th sample point. --> k 
There is data at the k-1'th sample point. --> k_1

There is data at the k'th sample point after measurement update --> km
There is data at the k-1'th sample point. --> k_1m
'''
#------------------------------------------
Xk      #State at k'th sample point
Xk_1    
Xkm
Xk_1m   


uk_1 = #get current in this variable 
ukm
uk_1m

""" Kalman hier regelen en overzetten naar uitproberen """

#------------------------------------------


Xk_1m       #get initialisation or previous estimate



#------------TIME UPDATE ------------------


Xk = Ak * Xk_1m + Bk * uk_1             #(1) state space update/ prediction

Pk = Ak * Pkv * (Ak.transpose()) + Qk   #(2) error covariance update


#------------MEASUREMENT UPDATE -----------


Hk = Pk * (Ck.transpose()) * #search for inverting matrices





