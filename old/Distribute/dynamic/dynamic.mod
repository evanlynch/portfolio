###DATA###
param numareas;
set areas = 1..numareas;

param numhours;
set hours=1..numhours;

param numassociates{areas, hours};

# door associated with an area
param dr{areas};

set areadoors{a in areas};

param numdoors;
set doors=1..numdoors;

param beta;
param cartlimit; 

# Expected CPH per store associated to a door
param Vol{doors, hours};
param Vol2{a in areas, i in areadoors[a], hours};

# Productivity target
param delta{areas};

# For looping purposes, select hour, then area
param hour;
param area;



###VARIABLES###
#Assignment variable
var X{i in areadoors[area], j in 1..numassociates[area, hour]: Vol2[area, i, hour] > 0} binary;

#Binary whether Assoc. is Used or Not
var Z{j in 1..numassociates[area, hour]} binary;

param load{a in areas, h in hours, j in 1..numassociates[a,h]};
param used{a in areas, h in hours, j in 1..numassociates[a,h]} binary;

#Deviational Under
var alpha{j in 1..numassociates[area, hour]} >=0;



###OBJECTIVE###
# Minimize total deviation
minimize deviation: sum{j in 1..numassociates[area, hour]} alpha[j];



###CONSTRAINTS###
subj to devfromgoal{j in 1..numassociates[area, hour]}: 
	sum{i in areadoors[area]: Vol2[area, i, hour] > 0} Vol2[area, i, hour]*X[i,j] >=  Z[j]*delta[area] - alpha[j];
	
subj to	assignonly1{i in areadoors[area]: Vol2[area, i, hour] > 0}: 
	sum{j in 1..numassociates[area, hour]} X[i,j] = 1;

subj to	dooradjacency{j in 1..numassociates[area, hour], i1 in areadoors[area], i2 in areadoors[area], i3 in areadoors[area]: i1<i2<i3 and Vol2[area, i1, hour] > 0 and Vol2[area, i2, hour] > 0 and Vol2[area, i3, hour] > 0}: 
	X[i2,j] >= X[i1,j] + X[i3,j] - 1;

subj to XZcst{i in areadoors[area], j in 1..numassociates[area, hour]: Vol2[area, i, hour] > 0}: 
	X[i,j] <= Z[j];

subj to ALPHAZcst{j in 1..numassociates[area, hour]}:
	alpha[j] <= delta[area]*Z[j];

subj to XZcst2{j in 1..numassociates[area, hour]}: 
	sum{i in areadoors[area]: Vol2[area, i, hour] > 0} X[i,j] >= Z[j];

subj to numberworkersassigned: 
	sum{j in 1..numassociates[area, hour]} Z[j] >= numassociates[area, hour]-1;

subj to loadlimit{j in 1..numassociates[area, hour]}: sum{i in areadoors[area]: Vol2[area, i, hour] > 0} Vol2[area, i, hour]*X[i,j] <= cartlimit;

subj to	maxlines{j in 1..numassociates[area, hour]}: 
	sum{i in areadoors[area]: Vol2[area, i, hour] > 0} X[i,j] <= beta;




