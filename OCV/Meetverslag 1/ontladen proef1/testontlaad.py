import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('meting1.csv')

df.plot(x='Timestamp', y=['Sl1Voltage', 'Sl2Voltage', 'Sl3Voltage', 'MVoltage', 'Current'])

plt.show()


