from gurobipy import *
from GurobiDATA import *
from GurobiMOD import *
from math import ceil
import pandas as pd
solutions = []
print(Vol)
numassociates = {}
#loop through hours, do stuff and solve
for hour in hours:
	
	numassociates[hour] = ceil(sum(Vol.loc[i,hour] for i in doors if i > 0)/delta)
	associates = range(1,numassociates[hour]+1)

	
	#BEGIN MOD FILE

	m = Model('DynamicResourceAllocation')

	#VARIABLES
	#Assignment of doors to associates
	X = m.addVars(doors,associates,vtype=GRB.BINARY)
	#Whether associate is used or not
	Z = m.addVars(associates,vtype=GRB.BINARY)
	#Deviation from goal
	alpha = m.addVars(associates,lb=0.0, vtype=GRB.CONTINUOUS)


	#OBJECTIVE FUNCTION
	m.setObjective(quicksum(alpha[j] for j in associates),GRB.MINIMIZE)


	#CONSTRAINTS
	m.addConstrs((sum(Vol.loc[i, hour] * X[i,j] for i in doors if Vol.loc[i,hour] > 0) >=  Z[j]*delta - alpha[j] for j in associates),"devfromgoal")
	m.addConstrs((sum(X[i,j] for j in associates) == 1 for i in doors if Vol.loc[i,hour]>0),"assignonly1")
	m.addConstrs((X[i2,j] >= X[i1,j] + X[i3,j] - 1 
		for j in associates for i1 in doors if Vol.loc[i1,hour]>0 for i2 in doors if Vol.loc[i2,hour]>0 for i3 in doors if Vol.loc[i3,hour]>0 if i1<i2<i3),"dooradjacency")
	m.addConstrs((X[i,j] <= Z[j] for i in doors for j in associates),"XZcst")
	m.addConstrs((alpha[j] <= delta*Z[j] for j in associates),"ALPHAZcst")
	m.addConstrs((quicksum(X[i,j] for i in doors) >= Z[j] for j in associates),"XZcst2")
	m.addConstr((quicksum(Z[j] for j in associates) >= numassociates[hour]-1),"numberworkersassigned")
	m.addConstrs((quicksum(Vol.loc[i,hour] * X[i,j] for i in doors)<= cartlimit for j in associates),"loadlimit")
	m.addConstrs((quicksum(X[i,j] for i in doors) <= beta for j in associates),"maxlines")

	#END MOD FILE


	#(load[area,hour,j] for j in range(1,numassociates[area,hour])) == sum(Vol2[area,i,hour]*X[i,j] for i in range(1,areadoors[area]) if Vol2[area,i,hour]>0)
	#used = {}
	#load = {}

	#for j in range(1,numassociates[hour]+1):
	#	load[hour,j] = sum(Vol[i,hour]*X[i,j] for i in doors if Vol[i,hour] > 0)

	#used[hour,j] for j in range(1,numassociates[hour]) == 0
	#for j in range(1,numassociates[hour]):
	#	if load[hour,j] > 0:
	#		used[hour,j] == 1
	m.optimize()
	obj = m.getObjective()
	solutions.append(obj.getValue())

for s in solutions:
	print('1: ', s)
'''productivity = {}
peopleUsed = {}

#Calculate productivity per associate in each major area
productivity[hour] = ((sum(load[hour,j] for j in range(numassociates[hour])) + sum(load[hour,j] for j in range(numassociates[hour]))) 
				 / (sum(used[hour,j] for j in range(numassociates[hour])) + sum(used[hour,j] for j in range(numassociates[hour]))))



#calculate total number of associates used 
peopleUsed[hour] = sum(used[hour,j] for j in range(numassociates[hour]))'''
