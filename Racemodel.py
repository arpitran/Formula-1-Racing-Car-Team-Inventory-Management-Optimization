from gurobipy import *
def solve(tyre,race,A,B,C):
    # Model
    m=Model("Inventory type")

    # Decision Variables
    x={}
    for j in race:
        for i in tyre:
            x[i,j]=m.addVar(vtype=GRB.CONTINUOUS, name='x_%s,%s' %(i,j))

    y={}
    for j in race:
        for i in tyre:
            y[i,j]=m.addVar(vtype=GRB.CONTINUOUS, name='y_%s,%s' %(i,j))

    I={}
    for j in race:
        for i in tyre:
            I[i,j]=m.addVar(vtype=GRB.CONTINUOUS, name='I_%s,%s' %(i,j))

    I1={}
    for j in race:
        for i in tyre:
            I1[i,j]=m.addVar(vtype=GRB.CONTINUOUS, name='I1_%s,%s' %(i,j))

    m.update()

    # Objective Function
    m.setObjective((quicksum(quicksum(C[i,j]*x[i,j] for i in tyre)for j in race))+(quicksum(quicksum(B[i,j]*x[i,j] for i in tyre)for r in race)), GRB.MINIMIZE)

    # Constraints
    for j in tyre:
        for i in race:
            if j==1:
                m.addConstr(I[i,j]==x[i,j]-D[i,j])

    for j in tyre:
        for i in race:
            if j==2:
                m.addConstr(I[i,j]==I[i,j-1]+x[i,j]-A[i,j])

    for i in tyre:
        for j in race:
            if j>2:
                m.addConstr(I[i,j]==I[i,j-1]+x[i,j]+y[i,j-2]-A[i,j])

    for i in tyre:
        for j in race:
            if j==1:
                m.addConstr(I1[i,j]==A[i,j]-y[i,j])

    for i in tyre:
        for j in race:
            if j>1:
                m.addConstr(I1[i,j]==I1[i,j-1]+A[i,j]-y[i,j])

    for t in tyre:
        for r in race:
            m.addConstr(x[t,r]<=100)
    
    m.optimize()

    print("Total cost %g" %m.objVal)
