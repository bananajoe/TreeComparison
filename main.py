from __future__ import absolute_import
from create_graph import *
from create_instances import * 
from lp_problem_grf import *
from compute_results import *
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
from copy import deepcopy

import time
import sys
import getopt
import json
import os.path
import zss
from six.moves import range

import collections

try:
    import numpy as np
    zeros = np.zeros
except ImportError:
    def py_zeros(dim, pytype):
        assert len(dim) == 2
        return [[pytype() for y in range(dim[1])]
                for x in range(dim[0])]
    zeros = py_zeros

try:
    from editdist import distance as strdist
except ImportError:
    try:
        from editdistance import eval as strdist
    except ImportError:
        def strdist(a, b):
            if a == b:
                return 0
            else:
                return 1

def insert_cost_delta(delta):
    def insert_cost(node):
        if (ExtendedNode.get_label(node) != 0):
            return strdist('', ExtendedNode.get_label(node))
        else:
            return delta
    return insert_cost

def remove_cost_delta(delta):
    def remove_cost(node):
        if (ExtendedNode.get_label(node) != 0):
            return strdist(ExtendedNode.get_label(node), '')
        else:
            return delta
    return remove_cost
    
#Calculate different tree edit distance
def compare_trees(tree_size, number_of_trees):
    print('Create instances')
    create_random_binary_trees(tree_size, number_of_trees)
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.json'
    print('Instances created successfully!')
    print('Instances can be found in ' + file_name)
    if os.path.exists(file_name):
        with open(file_name) as tree_file: 
            tree_list = json.load(tree_file)
            
        #Only compare with ated
        keys = {"ATED": 0.5, "CTED": 0, "STED": 1}
        
        size_start = time.time()
        for i in range(0, min(len(tree_list),number_of_trees)):
            #Loop output
            loop_time = time.time()
            j = i + 1
            needed_time = loop_time - size_start
            estimation = needed_time / j * number_of_trees
            print("(" + str(timedelta(seconds=round(needed_time))) + " / " + str(timedelta(seconds=round(estimation)))
                + ") (" + str(j) + "/" + str(number_of_trees) + ") tree size: " + str(tree_size))
                
            tree_one = create_binary_tree_from_list(tree_list[i]['one'])
            tree_two = create_binary_tree_from_list(tree_list[i]['two'])
            if ('one_adapted' not in tree_list[i]):
                tree_one_adapted = adapt_tree_one(tree_one, tree_two)
                tree_list[i]['one_adapted'] = tree_one_adapted.get_tree_list(tree_one_adapted)
            tree_one_adapted = create_binary_tree_from_list(tree_list[i]['one_adapted'])
            if ('#GRFRestr' not in tree_list[i]):
                I = compute_invalid_edges(tree_one.get_clusters(1), tree_two.get_clusters(1))
                tree_list[i]['#GRFRestr'] = len(I)
            #Compute gRF distance with varying 'k'
            for k in [1,4,16,64]:
                key = 'GRF' + str(k)
                if (key not in tree_list[i] and tree_size <= 32):
                    start = time.time()
                    print( "k is " + str(k))
                    lpProblem = createLPproblem(tree_one, tree_two, k)
                    lp = lpProblem.get("lp")
                    time_creation = time.time() - start
                    lp.solve()
                    c1 = lpProblem.get("c1")
                    c2 = lpProblem.get("c2")
                    if LpStatus[lp.status] == "Optimal":
                        end = time.time()
                        varsdict = {}
                        for v in lp.variables():
                            varsdict[v.name] = v.varValue
                        gRF = 0
                        for m in range(0,len(c1)):
                            gRF = gRF + 1
                            for l in range(0,len(c2)):
                                kex = "x_" + str(m) + "_" + str(l)
                                if (varsdict[kex] == 1.0):
                                    cup = [i for i in c1[m] if i in c2[l]]
                                    gRF = gRF - len(cup)/(len(c1[m]) + len(c2[l]) - len(cup))
                        for m in range(0,len(c2)):
                            used = 0
                            for l in range(0,len(c1)):
                                kex = "x_" + str(l) + "_" + str(m)
                                if (varsdict[kex] == 1.0):
                                    used = 1
                            if used == 0:
                                gRF = gRF + 1
                        solution = {'clusterOne': c1,
                                    'clusterTwo': c2,
                                    'vardsDict': json.dumps(varsdict)}
                        tree_list[i]['GRF' + str(k)] = {"cost": gRF, "time": end - start,
                        "time_creation": time_creation}
                        
            #Compute all TEDs defined in variable 'keys'
            for key,k in keys.items():
                if (key not in tree_list[i]):
                    start = time.time()
                    print(key)
                    cost = zss.distance(
                            tree_one, tree_two, tree_one.get_children,insert_cost_delta(k), remove_cost_delta(k),
                            update_cost=lambda a, b: strdist(ExtendedNode.get_label(a), ExtendedNode.get_label(b)))
                    end = time.time()
                    tree_list[i][key] = {"cost": cost, "time": end - start}
                key2 = key + "_a"
                if (key2 not in tree_list[i]):
                    start = time.time()
                    print(key2)
                    cost = zss.distance(
                            tree_one_adapted, tree_two, tree_one.get_children,insert_cost_delta(k), remove_cost_delta(k),
                            update_cost=lambda a, b: strdist(ExtendedNode.get_label(a), ExtendedNode.get_label(b)))
                    end = time.time()
                    tree_list[i][key2] = {"cost": cost, "time": end - start}

            with open(file_name, 'w') as outfile:
                json.dump(tree_list, outfile)
                

def main(argv):
    tree_size = 0
    number_of_trees = 0
    try:
       opts, args = getopt.getopt(argv,"ht:n:",["tree_size=","number_of_trees="])
    except getopt.GetoptError:
       print('main.py -t <tree_size> -n <number_of_trees>')
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -t <tree_size> -n <number_of_trees>')
            sys.exit()
        elif opt in ("-t", "--tree_size"):
            tree_size = int(arg)
        elif opt in ("-n", "--number_of_trees"):
            number_of_trees = int(arg)
        else:
            assert False, "unhandled option"
    if tree_size == 0 or number_of_trees == 0:
        print('Both arguments tree_size and number_of_trees are required!')
        print('main.py -t <tree_size> -n <number_of_trees>')
        sys.exit(2)
    return [tree_size, number_of_trees]

if __name__ == "__main__":
    tree_size, number_of_trees = main(sys.argv[1:])
    print('Size of trees is ', tree_size)
    print('Number of leaves file is ', number_of_trees)
    compare_trees(tree_size, number_of_trees)
    print('Create graphs')
    create_ted_to_grf1_graph(tree_size, number_of_trees)
    create_teds_graph(tree_size, number_of_trees)
    create_teds_difference_graph(tree_size, number_of_trees)
    create_teds_difference_adapted_graph(tree_size, number_of_trees)
    if number_of_trees == 300: 
        create_low_grf_high_ated_graph(tree_size, number_of_trees)
    else:
        print('To compute the low_grf_high_ated graph, set number_of_trees to 300')
    compute_results()
    create_time_graph()
