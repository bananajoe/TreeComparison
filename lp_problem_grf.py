#Additional function to create the ILP for the gRF

from pulp import *

def createLPproblem(tree_one, tree_two, k):
    clusters_one = tree_one.get_clusters(1)
    clusters_two = tree_two.get_clusters(1)
    c = compute_cost_function(clusters_one, clusters_two, k)
    #print(c)
    c1 = []
    for i in range(0,len(clusters_one)):
        c1.append(str(i))
    c2 = []
    for i in range(0,len(clusters_two)):
        c2.append(str(i))

    #Initialize LP Problem 
    lp = LpProblem("Tree Comparison general RF distance", -1)
    x =  LpVariable.dicts("x",(c1, c2),0,1,"Binary")

    #Objective function
    lp += lpSum([x[i][j] * c.get((i,j)) for i in c1 for j in c2]), "objective"

    # Constraints
    I = compute_invalid_edges(clusters_one, clusters_two)
    for i in c1:
        lp += lpSum([x[i][j] for j in c2]) <= 1, ""
    for j in c2:
        lp += lpSum([x[i][j] for i in c1]) <= 1, ""
    for k in I:
        lp += lpSum([x[str(k[0])][str(k[1])], x[str(k[2])][str(k[3])]]) <= 1, ""
    #print(clusters_one, clusters_two)
    
    return {"lp": lp, "c1": clusters_one, "c2": clusters_two}

def distance_between_clusters(cluster_one, cluster_two, k):
    cap = [i for i in cluster_one if i in cluster_two]
    in_second_but_not_in_first = [i for i in cluster_two if i not in cluster_one ]
    cup = cluster_one + in_second_but_not_in_first
    len_cap = float(len(cap))
    len_cup = float(len(cup))
    return 1 - (len_cap / len_cup)**k

def compute_cost_function(cluster_one, cluster_two, k):
    return {(str(i),str(j)): 2 - distance_between_clusters(cluster_one[i], cluster_two[j], k) for i in range(0, len(cluster_one)) for j in range(0, len(cluster_two))}

def compute_invalid_edges(clusters_one, clusters_two):
    I = []
    for (i,j,k,l) in [(i,j,k,l) for i in range(0,len(clusters_one))
                                for j in range(0,len(clusters_two))
                                for k in range(0,len(clusters_one))
                                for l in range(0,len(clusters_two))]:
        cap1 = [m for m in clusters_one[i] if m in clusters_one[k]]
        cap2 = [m for m in clusters_two[j] if m in clusters_two[l]]
        if len(cap1) == len(clusters_one[i]) and len(cap2) == len(clusters_two[j]):
            continue
        if len(cap1) == len(clusters_one[k]) and len(cap2) == len(clusters_two[l]):
            continue
        if len(cap1) == 0 and len(cap2) == 0:
            continue
        I.append([i,j,k,l])
   # print(I)
    return I
