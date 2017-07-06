import xlrd
import math
import numpy as np
import interpolatie as itp


#----------------------input variabelen ---------------------

file_location = r"C:\Users\Karel Van Peteghem\Documents\laatste jaar\MASTERPROEF batterijen\--------BMS programma---------\parameterwaarden.xlsx"
workbook = xlrd.open_workbook(file_location)

R0dischtable = workbook.sheet_by_index(0)
R0vtable = workbook.sheet_by_index(1)
R1table = workbook.sheet_by_index(2)
C1table = workbook.sheet_by_index(3)
R2table = workbook.sheet_by_index(4)
C2table = workbook.sheet_by_index(5)
R3table = workbook.sheet_by_index(6)
C3table = workbook.sheet_by_index(7)

#-------------------------------------------------------------


#let op: SOC2 en SOC1 hebben een andere betekenis dan die van verder in het programma.
    

def getR0(SOC1, SOC2, Ib, I_b, T):
    '''values without underscore are the k1'th (Ib) and values with underscore are the k+1'th (I_b) sample value'''
    
    meanIb = (Ib + I_b)/2.0 # 2.0 delen voor floats
    meanSOC = (SOC1 + SOC2)/2.0

    SOCValues = []
    IValues = []
    TValues = []

    sheet = R0dischtable
    #------------------if you want to change length of data, change these Values-----------
   
    rangeT = 4
    #--------------------------------------------------------------------------------------


    rangeSOC = 1
    value = 0
    delta = sheet.cell_value(3,0)-sheet.cell_value(2,0) 
    while (value < 1):
        value+=delta
        rangeSOC+=1

    for x in range(rangeSOC):
        SOCValues.append(sheet.cell_value(x+2,0))


    for x in range((sheet.nrows-2)/rangeSOC):
        IValues.append(sheet.cell_value((x+2)+(rangeSOC-1)*x,1))

    for x in range(rangeT):
        TValues.append(sheet.cell_value(0,4*x+1))

        
    Tmin = TValues[0]
    Tmax = TValues[len(TValues)-1]
    SOCmin = SOCValues[0]
    SOCmax = SOCValues[len(SOCValues)-1]
    Imin = IValues[0]
    Imax = IValues[len(IValues)-1]
    
    if (T >= Tmax):
        print("OUT OF RANGE Temperature, T =" + str(T) + " degreeCelsius")
        T=Tmax-0.0001
    
    if (T < Tmin):
        print("OUT OF RANGE Temperature, T =" + str(T)+ " degreeCelsius")
        T=Tmin
    
    if (meanIb >= Imax):
        print("OUT OF RANGE Current, I ="+ str(meanIb)+ " A")
        meanIb = Imax-0.0001
    
    
    if (meanIb < Imin):
        meanIb = Imin

    if (meanSOC >= SOCmax):
        print("OUT OF RANGE SOC, SOC ="+ str(meanSOC)+ " %")
        meanSOC=SOCmax-0.0001
    
    if (meanSOC < SOCmin):
        print("OUT OF RANGE SOC, SOC ="+ str(meanSOC)+ " %")
        meanSOC=SOCmin
    
    
    for x in range(rangeT):
        if (TValues[x] <= T and TValues[x+1] > T):
            Tup = TValues[x+1]
            Tunder = TValues[x]
            col1= 4*x
            col2 = 4*(x+1)
        


    for x in range(rangeSOC):
        if (SOCValues[x] <= meanSOC and SOCValues[x+1] > meanSOC):
            SOCup = SOCValues[x+1]
            SOCunder = SOCValues[x]
        


    for x in range(len(IValues)):
        if (IValues[x] <= meanIb and IValues[x+1] > meanIb):
            Iup = IValues[x+1]
            Iunder = IValues[x]
            rowstart = (x+2)+(rangeSOC-1)*x

    #start searching 4 values for Tunder

    ValuesInRow = []

    Values = []
    for x in range(rangeSOC*2):
    
        ValuesInRow.append(sheet.cell_value(rowstart+x,col1))
        ValuesInRow.append(sheet.cell_value(rowstart+x,col1+1))
        ValuesInRow.append(sheet.cell_value(rowstart+x,col1+2))

        num = 0
    
        if(SOCup == ValuesInRow[0] or SOCunder == ValuesInRow[0]):
            Values.append(ValuesInRow[2])
            num += 1
                                
        ValuesInRow = [] #reset ValuesInRow

                

    for x in range(rangeSOC*2):
    
        ValuesInRow.append(sheet.cell_value(rowstart+x,col2))
        ValuesInRow.append(sheet.cell_value(rowstart+x,col2+1))
        ValuesInRow.append(sheet.cell_value(rowstart+x,col2+2))

        num = 0
    
        if(SOCup == ValuesInRow[0] or SOCunder == ValuesInRow[0]):
            Values.append(ValuesInRow[2])
            num += 1
                                
        ValuesInRow = [] #reset ValuesInRow


    #Values sequence = T-I-SOC-,T-I-SOC+,T-I+SOC-,T-I+SOC+,T+I-SOC-,T+I-SOC+,T+I+SOC-,T+I+SOC+
    value1 = itp.getIntSOCValue(SOCup,SOCunder,meanSOC,Values[1],Values[0])
    value2 = itp.getIntSOCValue(SOCup,SOCunder,meanSOC,Values[3],Values[2])
    value3 = itp.getIntSOCValue(SOCup,SOCunder,meanSOC,Values[5],Values[4])
    value4 = itp.getIntSOCValue(SOCup,SOCunder,meanSOC,Values[7],Values[6])

    value10 = itp.getIntCurrentValue(Iup,Iunder,meanIb,value2,value1)
    value11 = itp.getIntCurrentValue(Iup,Iunder,meanIb,value4,value3)

    valuex = itp.getIntTemperatureValue(Tup,Tunder,T,value11,value10)
   
    return valuex
        
    

    
