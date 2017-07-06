
'''

there are still libraries to be imported.

The goal of this programm is to set up continuous
measurements of current and voltages of the slave and master cells.

It also creates the rows that will be used for recursion in SOC calculation.



TODO:

-fix everything with reading of data.
-interface zou nice zijn


'''






#----------------------------IMPORT------------------------------------

import math
import csv
import time as tm
import numpy as np

#----------------------------VARIABELEN--------------------------------

logtime = 0.5 #sampletime

global Total_capacity
Total_capacity = 120 #this value is in Ah

global cut_off_voltage_low
cut_off_voltage_low = 2.8

global cut_off_voltage_high
cut_off_voltage_high = 4.1

Tmax = 85   #degree celsius
Tmin = -45  #degree celsius

listOfData = [] #contains a row with all data from 1 timestamp



#-------------------------READ-IN----------------------------------------

""" Read in data from main script online measurements """

VoltageSlave1 = lib.readinVoltagecell(1)  
VoltageSlave2 = lib.readinVoltagecell(2)  
VoltageSlave3 = lib.readinVoltagecell(3)  
VoltageMaster = lib.readinVoltagecell(4)  

Current = lib.readinCurrent()            

T = lib.readinTemperature()              

t = time()  


#-------------------------Put all data in one row-----------------------


listOfData.append(VoltageSlave1)
listOfData.append(VoltageSlave2)
listOfData.append(VoltageSlave3)
listOfData.append(VoltageMaster)
listOfData.append(Current)
listOfData.append(T)
listOfData.append(SOC0)
listOfData.append(I1)
listOfData.append(I2)
listOfData.append(I3)
listOfData.append(tm.strftime("%H:%M:%S", tm.localtime()))

previousData = [] #these rows were originally meant for online parameter determination
nowData = []

#----------------------------------------------------------------------

global totalruntime
totalruntime = 0

#----------------------------------------------------------------------




while(listOfData[0] < cut_off_voltage_high and listOfData[1] < cut_off_voltage_high and listOfData[2] < cut_off_voltage_high and listOfData[3] < cut_off_voltage_high and listOfData[0] > cut_off_voltage_low and listOfData[1] > cut_off_voltage_low and listOfData[2] > cut_off_voltage_low and listOfData[3] > cut_off_voltage_low and abs(listOfData[4]) < 300 and listOfData[5] < Tmax and listOfData[5] > Tmin):

    print("programm running")
    
    if (totalruntime == 0):
        ''' initialize '''
        nowData = listOfData

        
        
        
    else





    

    VoltageSlave1 = lib.readinVoltagecell(1)  "this object is yet to be made"
    VoltageSlave2 = lib.readinVoltagecell(2)  "this object is yet to be made"
    VoltageSlave3 = lib.readinVoltagecell(3)  "this object is yet to be made"
    VoltageMaster = lib.readinVoltagecell(4)  "this object is yet to be made"
    Current = lib.readinCurrent()             "this object is yet to be made"

    listOfData.append(VoltageSlave1)
    listOfData.append(VoltageSlave2)
    listOfData.append(VoltageSlave3)
    listOfData.append(VoltageMaster)
    listOfData.append(Current)
    listOfData.append(tm.strftime("%H:%M:%S", tm.localtime()))
    

    start=tm.time()
    totalruntime += 1
    
    

    
    
    

 


    tm.sleep(logtime - (tm.time() - start))


    


    
    



    
