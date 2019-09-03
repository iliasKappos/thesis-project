import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from web3 import Web3

#connection with ganache
web3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
addresses=web3.eth.accounts #load the accounts of the ganache in an array

N=len(addresses)

balances=np.zeros((N))
totalGas=np.zeros((N))
spentEther=np.zeros((N))

#create a contract instance
contract_address="0x3Db6e2407F41EaE4D6f08e63e0d454F21121AC7a"
abi =json.loads('[ { "constant": false, "inputs": [], "name": "reset", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "resetWaiting", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "initialValue", "type": "int256" }, { "name": "i", "type": "uint256" } ], "name": "submitInitialValue", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "value", "type": "int256" }, { "name": "i", "type": "uint256" }, { "name": "iteration", "type": "uint16" } ], "name": "submitValue", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "updateY", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "name": "_whitelist", "type": "address[]" }, { "name": "_N", "type": "uint256" }, { "name": "_p", "type": "int256" }, { "name": "_Pd", "type": "int256" }, { "name": "_epsilon", "type": "int256" } ], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "constant": true, "inputs": [ { "name": "a", "type": "int256" }, { "name": "b", "type": "int256" } ], "name": "abs", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "pure", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "h", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "init", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "k", "outputs": [ { "name": "", "type": "uint16" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "l", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "N", "outputs": [ { "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "problemSolved", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "stillWaiting", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "address" } ], "name": "waiting", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "whitelist", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "x", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "y", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" }, { "name": "", "type": "uint256" } ], "name": "z", "outputs": [ { "name": "", "type": "int256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')
contract=web3.eth.contract(address=contract_address , abi=abi)

#read input-csv
basic_data = pd.read_csv('../Data/input.csv',header=None)
basic_data.columns = ['a','b','c','x_min','x_max','x','l','y','p','Pd']
a=np.array(basic_data['a'])
b = np.array(basic_data['b'])
c = np.array(basic_data['c'])
x_min = np.array(basic_data['x_min'])
x_max = np.array(basic_data['x_max'])
x_= np.array(basic_data['x'])
x = np.vstack((x_,np.zeros((1000,N))))
l_ = np.array(basic_data['l'])
l = np.vstack((l_,np.zeros((1000,N))))
y_ = np.array(basic_data['y'])
y = np.vstack((y_,np.zeros((1000,N))))
p=float(basic_data['p'][0])
Pd=int(basic_data['Pd'][0])

problemSolved = False
mul = 1000; #because solidity doed not support floats

#init ( send the initial values x[0][i])
k=0
for i in range(N):
 web3.eth.defaultAccount=addresses[i]
 tx_hash=contract.functions.submitInitialValue(int(x[k,i]*mul) ,i).transact()
 web3.eth.waitForTransactionReceipt(tx_hash,timeout=120)

diffx_y = np.zeros((1000))
diffy_y = np.zeros((1000))
#compute x[k+1][i]
while True:
    for i in range (N):
        print("")
        l[k][i]=contract.functions.l(k,i).call()
        y[k][i]=contract.functions.y(k,i).call()
        l[k][i] = l[k][i]/(mul)
        y[k][i] = y[k][i]/(mul)
        x[k+1,i]=min(max((p*y[k,i]-l[k][i]-b[i])/(2*a[i]+p),x_min[i]),x_max[i])
        web3.eth.defaultAccount=addresses[i]
        tx_hash=contract.functions.submitValue(int(x[k+1,i]*mul) ,i,k).transact()
        web3.eth.waitForTransactionReceipt(tx_hash,timeout=120)

    y[k+1][0]=contract.functions.y(k+1,0).call()
    diffx_y[k] = abs(x[k+1,0]-(y[(k+1),0]/1000))

    if k != 0:
        diffy_y[k-1] = y[(k),0] - y[(k-1),0]
    problemSolved = contract.functions.problemSolved().call()

    if(problemSolved==True):
        print("convergence",k)
        y[k+1][0]=contract.functions.y(k+1,0).call()
        diffy_y[k] = (y[(k+1),0]/1000) - y[(k),0]

        break
    k+=1
#compute the total gas per node and ether tah spent
for i in range (N):
    balances[i]=web3.eth.getBalance(addresses[i])
totalGas=(-balances+100.e+18)/(3.e+9)
spentEther=(-balances+100.e+18)/(1.e+18)
maxGas=np.max(totalGas)
minGas=np.min(totalGas)
averageGas=np.average(totalGas)
averageether=np.average(spentEther)

#plots
#evolution of power generation
figure1 = plt.figure(1)
for i in range(N):
    plt.plot(range(0,k+1),x[:k+1,i])

plt.ylabel('Power')
plt.xlabel('Iteration')
names = []
for i in range(0,20):
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
