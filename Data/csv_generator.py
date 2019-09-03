import numpy as np
import pandas as pd
import random

pd.options.mode.chained_assignment = None  # default='warn'

# read Number of lines from stdin
N = int(input("Give me number of lines (N): " ))

# read name of csv
name = input("Give me name of new csv file: ")

# create columns
a = np.around(np.random.uniform(low=0.038, high=0.08, size=(N,)),3)
b = np.random.randint(low=2, high=4, size=(N,))
c = np.around(np.random.uniform(low=5, high=9.2, size=(N,)),3)
x_min = np.random.randint(low=5, high=20, size=(N,))
x_max = np.random.randint(low=20, high=60, size=(N,))

x = np.zeros((N,),dtype=int)
xx = np.zeros((N,),dtype=int)
zeros = np.zeros((N,),dtype=int)

for i in range(N):
    x[i] = np.random.randint(x_min[i],x_max[i])
    xx[i] = np.random.randint(x_min[i],x_max[i])

sumOfx = int(np.sum(x))

concat_array = np.column_stack((a,b,c,x_min,x_max,x,zeros,x))
columns = ['a','b','c','x_min','x_max','x','zeros','xx']
df = pd.DataFrame(concat_array,columns=columns)
df = df.astype({'a': float, 'b': int, 'c': float, 'x_min': int, 'x_max': int, 'x': int, 'zeros': int, 'xx': int})
df['9'] = ''
df['9'][0] = '1'
df['10'] = ''
df['10'][0] = sumOfx

# write to csv
df.to_csv(name+'.csv', index=None, header=None)

print("The file with name ", name,".csv created!",sep="")
