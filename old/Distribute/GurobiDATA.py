from gurobipy import *
import pandas as pd

#numareas = 7

numhours = 5

numdoors = 5

cartlimit = 450

#Sets
#areas = range(1,numareas+1)
hours = range(1,numhours+1)

#areadoors = range(1,numareas+1)
doors = range(1,numdoors+1)

'''areas, dr = multidict({
	0: 41,
	1: 56,
	2: 70,
	3: 102,
	4: 111,
	5: 116,
	6: 129
	}) '''

'''areas, delta = multidict({
	0: 266,
	1: 266, 
	2: 170,
	3: 266,
	4: 170,
	5: 266,
	6: 170
	})'''
delta = 266
beta = 15

volData = 'volDataSmall.csv'
volData = pd.read_csv(volData,header=None)
Vol = pd.DataFrame(volData,index=doors,columns=hours)

