import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from web3 import Web3

web3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
print("Connection established")

addresses=web3.eth.accounts #load the accounts of the ganache in an array

N=len(addresses)

print("Komvoi einai ", N)

contract_address="0x3Db6e2407F41EaE4D6f08e63e0d454F21121AC7a"
abi =json.loads('[ { "constant": false, "inputs": [], "name": "reset", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "resetWaiting", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "initialValue", "type": "int256" }, { "name": "i", "type": "uint256" } ], "name": "submitInitialValue", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "value", "type": "int256" }, { "name": "i", "type": "uint256" }, { "name": "iteration", "type": "uint16" } ], "name": "submitValue", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "updateY", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "name": "_whitelist", "type": "address[]" }, { "name": "_N", "type": "uint256" }, { "name": "_p", "type": "int256" } ], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": true, "inputs": [ { "name": "a", "type": "int256" }, { "name": "b", "type": "int256" } ], "name": "abs", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "pure", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "h", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "init", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "k", "outputs": [ { "name": "", "type": "uint16" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "l", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "N", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "problemSolved", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "stillWaiting", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "waiting", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "whitelist", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "x", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "y", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "z", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')
contract=web3.eth.contract(address=contract_address , abi=abi)

print("Pernw to contract")

basic_data = pd.read_csv('../Data/input.csv',header=None)
basic_data.columns = ['a','b','c','x_min','x_max','x','l','y','p']
a=np.array(basic_data['a'])
b = np.array(basic_data['b'])
c = np.array(basic_data['c'])
x_min = np.array(basic_data['x_min'])
x_max = np.array(basic_data['x_max'])
x_= np.array(basic_data['x'])
x = np.vstack((x_,np.zeros((100,N))))
l_ = np.array(basic_data['l'])
l = np.vstack((l_,np.zeros((100,N))))
y_ = np.array(basic_data['y'])
y = np.vstack((y_,np.zeros((100,N))))
p=int(basic_data['p'][0])
#print("p ", p)
#print(a,b,c,x_min,x_max,x,l,y)
problemSolved = False
mul = 1000; #giati h solidity den exei float
print("Diavasa to csv kai dimiourgisa tous pinakes")

web3.eth.defaultAccount=addresses[0] # reset the problem
tx_hash=contract.functions.reset().transact()
web3.eth.waitForTransactionReceipt(tx_hash,timeout=120)

print("Ekana reset to problima")

k=0
for i in range(N):
 web3.eth.defaultAccount=addresses[i]
 print("Tha steilw to x[k,i] " , int(x[k,i]*mul))
 tx_hash=contract.functions.submitInitialValue(int(x[k,i]*mul) ,i).transact()
 web3.eth.waitForTransactionReceipt(tx_hash,timeout=120)

print("ekana to init")
diffx_y = np.zeros((100))
diffy_y = np.zeros((100))
while True:
    print("Arxi while loop me k = ",k)
    for i in range (N):
        print("")
        l[k][i]=contract.functions.l(k,i).call()
        y[k][i]=contract.functions.y(k,i).call()
        print("prin y = [",k,"][",i,"] ",y[k][i])
        print("prin l = [",k,"][",i,"] ",l[k][i])
        l[k][i] = l[k][i]/(mul)
        y[k][i] = y[k][i]/(mul)
        print("prin y = [",k,"][",i,"] ",y[k][i])
        print("prin l = [",k,"][",i,"] ",y[k][i])
        print("x[",k+1,"],",i,"]",(p*y[k,i]-l[k][i]-b[i])/(2*a[i]+p))
        x[k+1,i]=min(max((p*y[k,i]-l[k][i]-b[i])/(2*a[i]+p),x_min[i]),x_max[i])
        print("ypologisa to x[",k+1,"][",i,"] ", int(x[k+1][i]*mul))
        web3.eth.defaultAccount=addresses[i]
        tx_hash=contract.functions.submitValue(int(x[k+1,i]*mul) ,i,k).transact()
        web3.eth.waitForTransactionReceipt(tx_hash,timeout=120)
    diffx_y[k] = abs(x[k,0]-y[k,0])
    if k != 0:
        diffy_y[k-1] = y[(k),0] - y[(k-1),0]
    problemSolved = contract.functions.problemSolved().call()

    if(problemSolved==True):
        print("Ole",k)
        y[k+1][0]=contract.functions.y(k+1,0).call()
        print("prin y = [",k+1,"][",0,"] ",y[k+1][0])
        print("prin y = [",k+1,"][",0,"] ",y[k+1][0]/1000)
        diffy_y[k] = (y[(k+1),0]/1000) - y[(k),0]
        break


    print("Paw sto epomeno k ", k+1)
    k+=1


print("Paw na kanw ta plots")
#print(diffx_y)
print(diffy_y)
#evolution power
figure1 = plt.figure(1)
for i in range(N):
    plt.plot(range(0,k+1),x[:k+1,i])

plt.title('The evolution of the output powers.')
plt.ylabel('Power')
plt.xlabel('Iteration')
names = []
for i in range(0,10):
    names.append( 'P'+str(i))
plt.legend(names,loc='lower right')
#abs(x-y)

figure2 = plt.figure(2)
#for i in range(N):
plt.plot(range(0,k+1),diffx_y[:(k+1)])

plt.title(' The evolution of the primal residuals.')
plt.ylabel('Primal residual')
plt.xlabel('Iteration')


diffy_y = (-p)*diffy_y
#abs(y(k+1)-y(k))
figure3 = plt.figure(3)
#for i in range(N):
plt.plot(range(0,k+1),diffy_y[:(k+1)])

plt.title(' The evolution of the dual residuals.')
plt.ylabel('Dual residual')
plt.xlabel('Iteration')

figure4 = plt.figure(4)
sum_x = np.zeros((k+1))
for i in range(k+1):
    for j in range(N):
        sum_x[i]+=x[i,j]

pd_array = np.full((58,),150)
plt.plot(range(0,(k+1)),pd_array)
plt.plot(range(0,(k+1)),sum_x[:(k+1)])

plt.title('The evolution of the supply-demand balance')
plt.ylabel('Power')
plt.xlabel('Iteration')

plt.show()
