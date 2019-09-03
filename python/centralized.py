import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#read csv-input
basic_data = pd.read_csv('../Data/input.csv',header=None)
basic_data.columns = ['a','b','c','x_min','x_max','x','l','y','p','Pd']
a=np.array(basic_data['a'])
N=len(a)
b = np.array(basic_data['b'])
c = np.array(basic_data['c'])
x_min = np.array(basic_data['x_min'])
x_max = np.array(basic_data['x_max'])
x_= np.array(basic_data['x'])
x = np.vstack((x_,np.zeros((100000,N))))
l_ = np.array(basic_data['l'])
l = np.vstack((l_,np.zeros((100000,N))))
y_ = np.array(basic_data['y'])
y = np.vstack((y_,np.zeros((100000,N))))
p=float(basic_data['p'][0])
Pd=float(basic_data['Pd'][0])
h=np.zeros((100000))
z=np.zeros((100000,N))

problemSolved = False
k=0
diffx_y = np.zeros((100000))
diffy_y = np.zeros((100000))
# compute x[k+1][i]
while True:
    for i in range (N):
        x[k+1,i]=min(max((p*y[k,i]-l[k][i]-b[i])/(2*a[i]+p),x_min[i]),x_max[i])
#compute h[k] ,y[k+1][i], l[k+1][i]
    for i in range (N):
        if(i==0) :
            z[k][i]=x[k+1][i]+(l[k][i])/p;
        else :
            z[k][i]=z[k][i-1]+x[k+1][i]+(l[k][i])/p;

    h[k]=(p*((Pd)-z[k][N-1]))/N;

    for i in range (N):
      y[k+1][i]=(h[k]/p)+x[k+1][i]+(l[k][i])/p;
      l[k+1][i]=l[k][i]+p*(x[k+1][i]-y[k+1][i]);

#check for convergence
    counter=1
    for i in range (N) :
        if((abs(x[k+1][i]-y[k+1][i])<=0.1) and (abs(-p*(y[k+1][i]-y[k][i]))<=0.1)):
          counter=counter+1
    if(counter==N):
          problemSolved=True
    diffx_y[k] = abs(x[k+1,0]-y[(k+1),0])

    if k != 0:
        diffy_y[k-1] = y[(k),0] - y[(k-1),0]

    if(problemSolved==True):
        print("convergence in iteraton",k)
        diffy_y[k] = (y[(k+1),0]) - y[(k),0]

        break

    k+=1

#plots

#evolution of power generation
figure1 = plt.figure(1)
for i in range(N):
    plt.plot(range(0,k+1),x[:k+1,i])

plt.ylabel('Power')
plt.xlabel('Iteration')
names = []
for i in range(0,N):
    names.append( 'P'+str(i))
plt.legend(names,loc='lower right')

#evolution of primal residual of the first generator
figure2 = plt.figure(2)
plt.plot(range(0,k+1),diffx_y[:(k+1)])
plt.ylabel('Primal residual')
plt.xlabel('Iteration')


diffy_y = (-p)*diffy_y

#evolution of dual residual of the first generator
figure3 = plt.figure(3)
plt.plot(range(0,k+1),diffy_y[:(k+1)])
plt.ylabel('Dual residual')
plt.xlabel('Iteration')

#evolution of supply-demad balance
figure4 = plt.figure(4)
sum_x = np.zeros((k+2))

for i in range(k+2):
    for j in range(N):
        sum_x[i]+=x[i,j]

pd_array = np.full((k+1,),Pd)
plt.plot(range(0,(k+1)),pd_array)
plt.plot(range(0,(k+1)),sum_x[1:(k+2)])

plt.ylabel('Power')
plt.xlabel('Iteration')

plt.show()
