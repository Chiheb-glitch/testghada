import pandas as pd




import cv2 
import numpy as np 
import mediapipe as mp

#Dynamic methode (based on landmarks)
#ROI landmarks
area1 =[70,71,21,54,103,67,109,10,338,297,332,284,251,301,300,293,334,296,336,9,107,66,105,63,70] # forehead (Checked)
area2 = [113,124,156,143,116,117,228,25,130,113] # near_left_eye (Checked)
area3 = [342,353,383,372,345,346,448,255,359,342] # near_right_eye (Rectified)
area4 = [233,128,114,47,100,119,118,117,31,228,229,230,231,232,233] # under_left_eye (Checked)
area5 = [453,357,343,277,329,348,347,346,361,448,449,450,451,452,453] # under_right_eye (Rectified)
area6 = [55,8,285,417,351,6,122,193,55] # between_eyes (Rectified)
area7 = [185,186,216,207,192,135,169,170,211,204,106,43,146,61,185] # left_cheek (Rectified)
area8 = [409,410,436,427,416,364,394,395,431,424,335,273,375,291,409]  # right_cheek (Rectified)
area9 = [185,186,92,165,167,164,393,391,322,410,409,270,269,267,0,37,39,40,185] # over_lip (Rectified)
area10 = [57,43,106,182,83,18,313,406,335,273,287,375,321,405,314,17,84,181,91,146,57]  # under_lip (Changed)
area11 = [194,201,200,421,418,262,369,396,175,171,140,32,194] # chin (Rectified)


filename = "products.csv"
df = pd.read_csv(filename)
json_c={"Area 1": ["Wrinkles Depth Estimation on Average:", 0.04, ", Wrinkles detected: ", 6], 
    "Area 3": ["Wrinkles Depth Estimation on Average:", 0.05, ", Wrinkles detected: ", 15], 
    "Area 4": ["Wrinkles Depth Estimation on Average:", 0.05, ", Wrinkles detected: ", 22],
    }

    
t=[]
c=[]
for i in json_c:

   for index, row in df.iterrows():
    print('Index:', index)
    print('Row data:', row['Area'])
    if row["Area"] == i:
        t.append(df.iloc[index,:])
        c.append(index)

print(c)        
x=[]
intt=0
for i in t:
     
     y=[]
     y.append(i["Name"])
     y.append(i['Image URL'])
     y.append(i["Description"])
     y.append(i['Area'])
     y.append(c[intt])
     intt += 1 

     x.append(y)
print(x)




