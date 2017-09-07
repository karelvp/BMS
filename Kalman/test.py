import KalmanObject as kal

import pandas as pd




States = []
num = 0

karel = kal.getKalmanStart(3.292, 0.0, 25.0, 1.0) #initialisation of filter
"""

karel omvat nu een rij met 3 matrices.
In de eerste matrix zit de nieuwe geschatte staat
In de tweede matrix zit de covariantiematrix van de error tussen model en measuredvoltage --> P
In de derde matrix zit de error tussen het model en measured voltage

"""

States.append(karel[0].item(3,0))


while (num < 10000):

    karel = kal.getKalman1(karel, 3.292, 0.0, 25.0,1.0)

    States.append(karel[0].item(3,0))
    
    num += 1

    if(num == 190):
        print(karel[1])

df = pd.DataFrame({'Data': States})

writer = pd.ExcelWriter('States.xlsx', engine = 'xlsxwriter')

df.to_excel(writer, sheet_name='States')

writer.save()

print(States)


print('KLAAR')

