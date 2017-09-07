import KalmanObject as kal

import pandas as pd

import xlrd
#-------------------------READ-IN----------------------------------------


file_location = r"C:\Users\Karel Van Peteghem\Documents\MATLAB\Scripts\DDPT\ModelV.xlsx"
file_location2 = r"C:\Users\Karel Van Peteghem\Documents\MATLAB\Scripts\DDPT\Stroom.xlsx"
file_location3 = r"C:\Users\Karel Van Peteghem\Documents\MATLAB\Scripts\DDPT\MeasuredV.xlsx"
workbookmodel = xlrd.open_workbook(file_location)
workbookstroom = xlrd.open_workbook(file_location2)
workbookmeasured = xlrd.open_workbook(file_location3)

modelV = workbookmodel.sheet_by_index(0)
stroom = workbookmodel.sheet_by_index(0)
measuredV = workbookmodel.sheet_by_index(0)

#-------------------------init----------------------------------------

States = []
num = 0

tijd = measuredV.cell_value(0,0)
tijd2 = measuredV.cell_value(1,0)
Volt1 = measuredV.cell_value(0,1)
Volt2 = measuredV.cell_value(1,1)
cur1 = stroom.cell_value(0,1)
cur2 = stroom.cell_value(1,1)


karel = kal.getKalmanStart(Volt1, 0.0, 25.0, 1.0) #initialisation of filter

States.append(karel[0].item(3,0))

#-------------------------logging----------------------------------------

while (num < 36000):

    if(abs(stroom.cell_value(num+1,1)) <1.0):
        Stroom = 0.0
    else:
        Stroom = float(stroom.cell_value(num+1,1))

    karel = kal.getKalman1(karel, float(measuredV.cell_value(num+1,1)),Stroom,25.0, float(measuredV.cell_value(num+1,0)- measuredV.cell_value(num,0)))

    print(karel[0].item(3,0))
    
    States.append(karel[0].item(3,0))
    
    num += 1


df = pd.DataFrame({'Data': States})

writer = pd.ExcelWriter('StatesMeasuredV.xlsx', engine = 'xlsxwriter')

df.to_excel(writer, sheet_name='States')

writer.save()


print('KLAAR')    
