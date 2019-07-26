
from gurobipy import *

areas, dr = multidict({
	0: 41,
	1: 56,
	2: 70,
	3: 102,
	4: 111,
	5: 116,
	6: 129
	}) 








areadoors = [0,0,0,0,0,0,0]
area = 0
hour = 0
areadoors[0] = range(1,dr[0])
areadoors[1] = range(dr[0],dr[1])
areadoors[2] = range(dr[1],dr[2])
areadoors[3] = range(dr[2],dr[3])
areadoors[4] = range(dr[3],dr[4])
areadoors[5] = range(dr[4],dr[5])
areadoors[6] = range(dr[5],dr[6])

print(areadoors[5])

areadoorz = [range(1,dr[0]),range(dr[0],dr[1]),range(dr[1],dr[2]),range(dr[2],dr[3]),range(dr[3],dr[4]),range(dr[4],dr[5]),range(dr[5],dr[6])]