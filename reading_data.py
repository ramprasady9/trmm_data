
import pandas as pd
df=pd.read_csv('/home/ram/Documents/trmm_calc/India_clip.csv')

print(df["rowid"][1:5])

import matplotlib.pyplot as pp
pp.plot(df['long'],df['lat'])