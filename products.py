import pandas as pd


import numpy as np 
import mediapipe as mp


def filter_data_frame_by(df,param1,param2):
 t=[]
 for index, row in df.iterrows():

    if row[param1] == param2:
        t.append(df.iloc[index,:])
 return t

def filter_data_frame_from_to(df,param1,param2,param3):
 t=[]
 for index, row in df.iterrows():

    if (float(row[param1]) >=   param2 ) and (float(row[param1] )<= param3 ):
        t.append(df.iloc[index,:])
 return t
  





filename = "_products.csv"
df = pd.read_csv(filename)

    



x=filter_data_frame_by(df,"Label","Moisturizer")
print(x)
y=filter_data_frame_from_to(df,"Price (Euro)",150,350)
print(y)
#najem nesta3melha fi rating zeda

y=filter_data_frame_from_to(df,"Online Review",4,5)
print(y)




