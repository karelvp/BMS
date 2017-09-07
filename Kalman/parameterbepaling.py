import interpolatie as itp




#-------------------------------------------------------------



def getVal2(SOC, T, sheet):

    meanSOC = SOC
    

    SOCValues = []

    rangeSOC = 1
    value = sheet.cell_value(2,0)
    delta = sheet.cell_value(3,0)-sheet.cell_value(2,0) 
    while (value < 90.08679245):#change value for max soc
        value+=delta
        rangeSOC+=1

  
    for x in range(rangeSOC):
        SOCValues.append(sheet.cell_value(x+2,0))

  
    col1 = 0
  

    for x in range(rangeSOC):
        if (SOCValues[x] <= meanSOC and SOCValues[x+1] > meanSOC):
            SOCup = SOCValues[x+1]
            SOCunder = SOCValues[x]


    ValuesInRow = []

    Values = []
    for x in range(rangeSOC):
    
        ValuesInRow.append(sheet.cell_value(1+x,col1))
        ValuesInRow.append(sheet.cell_value(1+x,col1+1))
        ValuesInRow.append(sheet.cell_value(1+x,col1+2))


        num = 0
    
        if(SOCup == ValuesInRow[0] or SOCunder == ValuesInRow[0]):
            Values.append(ValuesInRow[2])
            num += 1
                                
        ValuesInRow = [] #reset ValuesInRow


    #Values sequence = T-I-SOC-,T-I-SOC+,T-I+SOC-,T-I+SOC+,T+I-SOC-,T+I-SOC+,T+I+SOC-,T+I+SOC+
    value1 = itp.getIntSOCValue(SOCup,SOCunder,meanSOC,Values[1],Values[0])



   
    return value1










def getVal3(SOC, T, sheet):

    meanSOC = SOC

    

    SOCValues = []

    rangeSOC = 1
    value = 0.0 #startvalue SOC
    delta = sheet.cell_value(3,0)-sheet.cell_value(2,0) 
    while (value < 99.89):#change value for max soc
        value+=delta
        rangeSOC+=1

   

    for x in range(rangeSOC):
        SOCValues.append(sheet.cell_value(x+2,0))

    col1 = 0



    for x in range(rangeSOC):
        if (SOCValues[x] <= meanSOC and SOCValues[x+1] > meanSOC):
            SOCup = SOCValues[x+1]
            SOCunder = SOCValues[x]


    


    ValuesInRow = []

    Values = []
    for x in range(rangeSOC):
    
        ValuesInRow.append(sheet.cell_value(1+x,col1))
        ValuesInRow.append(50.0)
        ValuesInRow.append(sheet.cell_value(1+x,col1+1))

        num = 0
    
        if(SOCup == ValuesInRow[0] or SOCunder == ValuesInRow[0]):
            Values.append(ValuesInRow[2])
           
            num += 1
                                
        ValuesInRow = [] #reset ValuesInRow

    
    value1 = Values[1]



   
    return value1









    
    
        

def getVal(SOC, Ib, T, sheet):
    
    meanIb = Ib 
    meanSOC = SOC

    SOCValues = []
    IValues = []
    TValues = []

    


    rangeSOC = 1
    value = 0.698113207547166 #startvalue SOC
    delta = sheet.cell_value(3,0)-sheet.cell_value(2,0) 
    while (value < 86.63584906):#change value for max soc
        value+=delta
        rangeSOC+=1

    for x in range(rangeSOC):
        SOCValues.append(sheet.cell_value(x+2,0))


    for x in range((sheet.nrows-2)/rangeSOC):
        IValues.append(sheet.cell_value((x+2)+(rangeSOC-1)*x,1))

  
    SOCmin = SOCValues[0]
    SOCmax = SOCValues[len(SOCValues)-1]
    Imin = IValues[0]
    Imax = IValues[len(IValues)-1]

  
    
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
    
    
    col1 = 0


    for x in range(rangeSOC):
        if (SOCValues[x] <= meanSOC and SOCValues[x+1] > meanSOC):
            SOCup = SOCValues[x+1]
            SOCunder = SOCValues[x]
        


    for x in range(len(IValues)):
        if (IValues[x] <= meanIb and IValues[x+1] > meanIb):
            Iup = IValues[x+1]
            Iunder = IValues[x]
            rowstart = (x+2)+(rangeSOC-1)*x

    
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




    #Values sequence = T-I-SOC-,T-I-SOC+,T-I+SOC-,T-I+SOC+,T+I-SOC-,T+I-SOC+,T+I+SOC-,T+I+SOC+
    value1 = itp.getIntSOCValue(SOCup,SOCunder,meanSOC,Values[1],Values[0])
    value2 = itp.getIntSOCValue(SOCup,SOCunder,meanSOC,Values[3],Values[2])


    value10 = itp.getIntCurrentValue(Iup,Iunder,meanIb,value2,value1)



   
    return value10
        
    

    
