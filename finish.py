import pandas as pd

# create a sample dataframe
filename = "_products.csv"
df = pd.read_csv(filename)
# initialize an empty list to store values in column 'x' from 5 to 20
ch =""

# loop through the dataframe and append the values in column 'x' to the list if they are between 5 and 20
for index, row in df.iterrows():
    if index >= 551  and index <= 580:
        ch += "," + row['Full Name']
with open('output.txt', 'w') as f:
    f.write(ch)

