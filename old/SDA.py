##############################################################
###                DYNAMIC ALLOCATION MODEL                ###
##############################################################

from gurobipy import *
import pandas as pd
import numpy as np
from math import ceil

##############################################################
###             DATA INITIALIZING & PROCESSING             ###
##############################################################

#set the number of hours to solve for
numhours = 4

#set the number of loading docks in the facility
numdoors = 129

#create ranges for hours and doors
hours = range(1,numhours+1)
doors = range(1,numdoors+1)

#set how many areas in the facility (test model had a max size of 41 doors)
numareas = 2

#set goal load per associate for each area
'''areas, goal = multidict({
    1: 266,
    2: 100, 
    })'''
areas, goal = multidict({
    1: 266,
    2: 266, 
    3: 170,
    4: 266,
    5: 170,
    6: 266,
    7: 170
    })

#set the last door in each area
'''areas, lastDoorInArea = multidict({
    1: 5,
    2: 10,
    }) '''
areas, lastDoorInArea = multidict({
    1: 41,
    2: 56,
    3: 70,
    4: 102,
    5: 111,
    6: 116,
    7: 129
    }) 

#create the sets of doors that make up each area
areaDoors = {}
for area in areas:
    if area == 1:
        areaDoors[area] = range(1,lastDoorInArea[area]+1)
    else: 
        areaDoors[area] = range(lastDoorInArea[area-1]+1,lastDoorInArea[area]+1)

#set the limit of load size for any given associate
loadLimit = 450

#set the limit on the number of lines any given associate can be assigned
lineLimit = 17

#pull in volume matrix
volData = 'volDataFull.csv'
volData = pd.read_csv(volData,header=None)
Vol = pd.DataFrame(volData,index=doors,columns=hours)

#create subsets of volume by area of the facility, such that you have a volume for any given area,door,hour combination
areaAreaDoorHour, Vol2 = multidict({'':0}) 
for a in areas:
    for i in areaDoors[a]:
        for h in hours:
            Vol2[a,i,h] = Vol.loc[i,h]
del Vol2['']

#initialize sets for solutions, assignments and numassociates
solutions = {}
assignments = {}
numassociates = {}

##############################################################
###                         MODEL                          ###
##############################################################

#define model and set time limit on solution
m = Model('DynamicResourceAllocation')
m.setParam('TimeLimit', 60)

#loop through each area and hour,create model, solve, execute post-processing
for hour in hours:
    for area in areas:
        #determine the number of associates required by volume for the hour
        numassociates[area,hour] = ceil(sum(Vol2[area,door,hour] for door in areaDoors[area] if Vol2[area,door,hour] > 0)/goal[area])

        #set the range of associates
        associates = range(1,numassociates[area,hour]+1)

        ''' ----- DECISION VARIABLES -----  '''

        #Assignment of doors to associates
        X = m.addVars(areaDoors[area],associates,vtype=GRB.BINARY,name='X')
        #Whether associate is used or not
        Z = m.addVars(associates,vtype=GRB.BINARY,name='Z')
        #Deviation under goal
        alpha = m.addVars(associates,lb=0.0, vtype=GRB.CONTINUOUS,name='alpha')

        # ----- OBJECTIVE FUNCTION ----- #

        m.setObjective(quicksum(alpha[j] for j in associates),GRB.MINIMIZE)

        ''' ----- CONSTRAINTS ----- '''

        '''For any associate in the set of associates that are calculated as needed in that area and hour, 
        the sum of volume going to the doors that associate is assigned must be greater than or equal to 
        the goal, minus the underachievement.'''
        m.addConstrs((sum(Vol2[area,i, hour] * X[i,j] for i in areaDoors[area] if Vol2[area, i, hour] > 0) 
            >=  Z[j]*goal[area] - alpha[j] for j in associates),"devFromGoal")

        '''Ensure that associates are only assigned to doors that are adjacent to each other. 
        If a door has a volume of zero, it will skip the consideration of assigning an associate 
        to that door, and thus the next adjacent door can be assigned.'''
        m.addConstrs((X[i2,j] >= X[i1,j] + X[i3,j] - 1 
            for j in associates for i1 in areaDoors[area] if Vol2[area,i1,hour]>0 
            for i2 in areaDoors[area] if Vol2[area,i2,hour]>0 for i3 in areaDoors[area] if Vol2[area,i3,hour]>0 
            if i1<i2<i3),"doorAdjacency")

        '''Ensure that a door is assigned to one associate and only one.'''
        m.addConstrs((sum(X[i,j] for j in associates) == 1 for i in areaDoors[area] if Vol2[area, i, hour] > 0),"assignOnly1")

        '''Ensure that if a door has no volume in a given hour, it must not be assigned.'''
        m.addConstrs((sum(X[i,j] for j in associates) == 0 for i in areaDoors[area] if Vol2[area, i, hour] == 0),"doNotAssignZeroVolDoor")
        
        '''Binary switching constraints. If a door is assigned an associate, that associate must be considered as used.'''
        m.addConstrs((X[i,j] <= Z[j] for j in associates for i in areaDoors[area] if Vol2[area, i, hour] > 0),"usedBinarySwitch")

        '''If an associate is to be used, they must be assigned to at least one door.'''
        m.addConstrs((quicksum(X[i,j] for i in areaDoors[area]) >= Z[j] for j in associates),"assignedBinarySwitch")

        '''Ensure that the deviation for an associate does not exceed the goal for that associate (don't completely understand this) '''
        m.addConstrs((alpha[j] <= goal[area]*Z[j] for j in associates),"IDK")

        '''The model has to use the number of associates that are calculated as needed in the area and hour,
        minus one associate if it can find a way to feasibly do so.'''
        m.addConstr((quicksum(Z[j] for j in associates) >= numassociates[area,hour]-1),"minusOneIfPossible")

        '''Ensure that the volume assigned to an associate across doors to not exceed a certain number of cartons.'''
        m.addConstrs((quicksum(Vol2[area,i,hour] * X[i,j] for i in areaDoors[area]) <= loadLimit for j in associates),"loadLimit")

        '''Ensure that the number of doors an associate is assigned never exceeds a certain number.'''
        m.addConstrs((quicksum(X[i,j] for i in areaDoors[area]) <= lineLimit for j in associates),"lineLimit")

        ''' ----- BEGIN RUN ----- '''
        print('Hour: ',hour)
        print('Area: ',area)

        #allow optimization to run in the background without displaying all the output; solve
        m.setParam( 'OutputFlag', False )
        m.optimize()
        print(m.getAttr('Status'))

        ''' ----- POST-SOLUTION PROCESSING ----- '''

        #obj = m.getObjective()
        #solutions[area,hour] = obj.getValue()

        #calculate the load per used associate and whether associate was used
        load = {}
        used = {}
        totalUsed = 0
        for j in associates: 
            load[area,hour,j] = sum(Vol2[area,i,hour]*X[i,j].x for i in areaDoors[area] if Vol2[area,i,hour]>0)
            if load[area,hour,j] > 0:
                used[area,hour,j] = 1
            else: 
                used[area,hour,j] = 0
            totalUsed += used[area,hour,j]

        #create a dataFrame for the hour, which will contain the associate to door assignments
        assignments[area,hour] = pd.DataFrame(data=None,index=areaDoors[area],columns=associates)    
        for i in areaDoors[area]:
             for j in associates:
                if X[i,j].x == 1:
                    assignments[area,hour].loc[i,j] = X[i,j].x
                else:
                    assignments[area,hour].loc[i,j] = ''
                for assignment in assignments:
                    fileName = "".join(["resultsArea",str(area),"Hour",str(hour),".csv"])
                    assignments[assignment].to_csv(fileName)
        #calculate the area productivity
        productivity = {}

        
        ''' ----- DISPLAY OUTPUT ----- '''
        
        print('# Associates Required by Volume: ',numassociates[area,hour])
        print('# Associates Used: ',totalUsed)
        print('Assignments:')
        print(assignments[area,hour])
        print('Load per Associate: ')
        for j in associates:
            print(j,'(',used[area,hour,j],')',': ',load[area,hour,j],'|',alpha[j].x)
        print('Total volume not expected to load (objective): ',m.getObjective().getValue())
        print('++++++++++++++++++++')
        print('')