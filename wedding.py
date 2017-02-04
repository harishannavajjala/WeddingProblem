"""
Initial State:- is an N*N matrix (with all values set to 0) . 'N' is the total number of persons
Goal State   :- In the matrix columns correspond to tables and rows correspond to persons i.e., if there is a 1 at a location i,j
                in my matrix it means that person 'i' is on table 'j'. All the persons in a column shouldn't be friends with each other and
                number of persons in one column/table should not exceed the maximum limit per table.
                So, the # of 1's on every column should be less than that limit.

successor function:- Consider a current state S. Assume it has x persons already sitting in the banquet hall. Every time our successor function
                     adds one new person to some table on the banquet hall. So, this person could selected in N-x ways. So, there would be
                    N-x new genereated states.

Cost function:-    Every newly generated state costs one unit as it adds one new person to the banquet hall.

Hueristic function:- Our heuristic function is a sum of g(s) and h(s). g(s) is based on the cost that incurred in reaching the state i.e.,
                    the number of tables that are currently occupied. And h(s) is an estimation of the number of tables that it might consume
                    in future. h(s) depends on the quantities like - sum of the number of friends each remaining guy has and total number of
                    guys that still need to be seated. This heuristic never overestimates the total number of tables consumed.
                    HENCE, our heuristic is admissable.

"""
import copy
import sys
x = 0

# This function checks if a given state is a goal state or not and returns a boolean value
def test_goal(current_state,fatrix):
    global x
    x+=1

    flag = True
    for i in range(0,len(fatrix[0])):
        if(sum(current_state[i])!=1):
            flag=False
            break
    return flag

#This function generates a friendship matrix. Every row and column represents a person. If there is a value 1 at a location
#   i,j then that means person at location 'i' and person at location 'j' are friends.
def generate_Fatrix(lines):
    uQnames = []
    for line in lines:
        line = line.strip()
        names = line.split()
        for name in names:
            if(name not in uQnames):
                uQnames.append(name)
    fatrix = [[0] * len(uQnames) for _ in range(len(uQnames))]
    for line in lines:
        line = line.strip()
        names = line.split()
        i=0
        for j in range(1,len(names)):
            fatrix[uQnames.index(names[i])][uQnames.index(names[j])] = 1
            fatrix[uQnames.index(names[j])][uQnames.index(names[i])] = 1

    i = 0
    j = 0
    while(i<len(uQnames) and j<len(uQnames)):
        fatrix[i][j] = -1
        i+=1
        j+=1

    return uQnames,fatrix

#This method checks if given two persons are friends or not and returns a boolean value
def check_friendship(i,ind,fatrix):
    if(fatrix[i][ind])==1:
        return True
    else:
        return False

#This function computes the hueristic value of a newly generated state
def findHeuristic(next_state,fatrix):
    tcount = 0
    totalsum = sum([ sum(row) for row in fatrix ] )+len(fatrix)
    flag = False
    pcount = 0
    h=0
    for j in range(len(fatrix)):
        for i in range(len(fatrix)):
            if (next_state[i][j] == 1):
                pcount+=1
                totalsum -= (sum(fatrix[i]) + 1)
                flag = True
        if flag:
            tcount += 1
            flag = False

    h = totalsum + tcount
    if(not (len(fatrix)==pcount)):
        h = 0.45*tcount + (totalsum / float(len(fatrix) - pcount))
    else:
        h = 0.45*tcount
    return h

#This function inserts a given person into the current set of tables and generates a new state
def insert_person(current_state,name,uQnames,fatrix):
    ind = uQnames.index(name)
    next_state = None
    flag = False
    sum_col = 0
    h=0

    for j in range(0,len(uQnames)):
        sum_col = 0
        for i in range(0,len(uQnames)):
            if(current_state[i][j] != -1):
                sum_col+=current_state[i][j]
        if(sum_col>=spt):
            continue
        for i in range(0, len(uQnames)):
            if(current_state[i][j]==1 and check_friendship(i,ind,fatrix)):
                flag = True
                break
        if flag:
            flag = False
            continue

        next_state = copy.deepcopy(current_state)
        next_state[ind][j] = 1
        h = findHeuristic(next_state,fatrix)
        break
    return next_state,h

#This function generates successor states for any given state
def successor(current_state,uQnames,fatrix):
    global x
    s_states = []
    for name in uQnames:
        if sum(current_state[uQnames.index(name)])==0:
            x += 1
            next_state,h=insert_person(current_state,name,uQnames,fatrix)
            if(next_state!=None):
                s_states.append((next_state,h))
    return s_states

#This function appends newly generated states to the fringe
def appendToFringe(s_states,fringe):
    for state in s_states:
        fringe.append(state)

#This function selects a state from fringe which has least heuristic value
def findCurrentState(fringe):
    if (len(fringe) == 1):
        x = fringe.pop(0)
        curr = x[0]
        #g = x[2]
    else:
        minhue = fringe[0][1]
        curr = fringe[0][0]
        icurr = 0
        # move = fringe[0][3]
        for i in range(1, len(fringe)):
            if (fringe[i][1] < minhue):
                minhue = fringe[i][1]
                icurr = i
        curr = fringe[icurr][0]
        #g = fringe[icurr][2]
        fringe.pop(icurr)

    return curr

#This function prints the final output
def printBanquetHall(current_state,uQnames):
    tcount = 0
    for j in range(len(fatrix)):
        for i in range(len(fatrix)):
            if (current_state[i][j] == 1):
                flag = True
                tcount += 1
                break

    tcount = str(tcount)
    tcount+= " "

    for j in range(len(uQnames)):
        colFirst = True
        for i in range(len(uQnames)):
            if(current_state[i][j]==1):
                if(colFirst):
                    tcount+= uQnames[i]
                    colFirst = False
                else:
                    tcount += ","+uQnames[i]
        tcount+= " "
    print tcount

spt=int(sys.argv[2]) #This is the max number of seats per table
file = open(sys.argv[1],"r")
lines = file.readlines()
file.close()
uQnames,fatrix=generate_Fatrix(lines)
np = len(uQnames) #Total number of persons

initial_state = [[0]*np for _ in range(np)]
fringe = []
fringe.append((initial_state,0))

while len(fringe)>0:
    current_state = findCurrentState(fringe)
    if (test_goal(current_state,fatrix)):
        printBanquetHall(current_state,uQnames)
        break
    s_states=successor(current_state,uQnames,fatrix)
    appendToFringe(s_states,fringe)
