from __future__ import absolute_import
from extended_node import ExtendedNode
from datetime import datetime
from datetime import timedelta
from pulp import *
from matplotlib import pyplot as plt
from copy import deepcopy

import catalan_numbers
import random
import time
import json
import os
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

def random_full_binary_tree(n):
    if n == 1:
        return ExtendedNode(n)
    else:
        catalan = catalan_numbers.load_catalan_numbers_until(n)
        lower = 0
        r = random.random()
        for i in range(1,n):
            p = (catalan[i-1] / float(catalan[n-1]) * catalan[n-i-1])
            upper = lower + p
            if lower <= r and r < upper:
                break
            lower = upper
        return ExtendedNode(n, [random_full_binary_tree(i), random_full_binary_tree(n-i)])

def random_full_binary_tree_stack(n):
    root = ExtendedNode(n)
    stack = [root]
    pstack = []
    while len(stack) > 0:
        node = stack.pop()
        pstack.append(node)
        n = node.get_label(node)
        if n > 1:
            catalan = catalan_numbers.load_catalan_numbers_until(n)
            lower = 0
            r = random.random()
            for i in range(1,n):
                p = (catalan[i-1] * catalan[n-i-1]) / float(catalan[n-1])
                upper = lower + p
                if lower <= r and r < upper:
                    break
                lower = upper
            left = ExtendedNode(i)
            node.addkid(left)
            stack.append(left)
            right = ExtendedNode(n-i)
            node.addkid(right)
            stack.append(right)

    return root

def create_random_binary_trees(tree_size, number_of_trees):
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.json'

    if os.path.exists(file_name):
        with open(file_name) as tree_file: 
            tree_list = json.load(tree_file)
    else:
        tree_list = []

    current_list_length = len(tree_list)
    safety_net = 0
    while current_list_length < number_of_trees and safety_net < 10 * number_of_trees:
        new_tree_one_list = random_full_binary_tree_stack(tree_size)
        new_tree_one_list.label_leaves_randomly()
        new_tree_one_list = new_tree_one_list.get_tree_list(new_tree_one_list)
        new_tree_two_list = random_full_binary_tree_stack(tree_size)
        new_tree_two_list.label_leaves_randomly()
        new_tree_two_list = new_tree_two_list.get_tree_list(new_tree_two_list)
        append = 0
        if new_tree_one_list.__str__() != new_tree_two_list.__str__():
            append = 1
            new_tree_list = {"one": new_tree_one_list,"two": new_tree_two_list}
            for tree in tree_list:
                if new_tree_list.__str__() == tree.__str__():
                    append = 0
                    break

        if append == 1:
            tree_list.append(new_tree_list)
            current_list_length = current_list_length + 1
        safety_net = safety_net + 1

    with open(file_name, 'w') as outfile:
        json.dump(tree_list, outfile)

def create_binary_tree_from_list(list):
    if len(list) == 1:
        return ExtendedNode(list[0])
    elif len(list) == 2:
        node = ExtendedNode(0, [create_binary_tree_from_list(list[0]), create_binary_tree_from_list(list[1])])
        node.fix_tree_list()
        return node

def distance_between_clusters(cluster_one, cluster_two, k):
    cap = [i for i in cluster_one if i in cluster_two]
    in_second_but_not_in_first = [i for i in cluster_two if i not in cluster_one ]
    cup = cluster_one + in_second_but_not_in_first
    len_cap = float(len(cap))
    len_cup = float(len(cup))
    return 1 - (len_cap / len_cup)**k

def compute_cost_function(cluster_one, cluster_two, k):
    return {(str(i),str(j)): distance_between_clusters(cluster_one[i], cluster_two[j], k) for i in range(0, len(cluster_one)) for j in range(0, len(cluster_two))}

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
    return I

def createLPproblem(tree_one, tree_two, k):
    clusters_one = tree_one.get_clusters(1)
    clusters_two = tree_two.get_clusters(1)
    c = compute_cost_function(clusters_one, clusters_two, k)
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

    
    return lp

def adapt_tree_one(tree_one, tree_two):
    stack = list()
    one_copy = deepcopy(tree_one)
    stack.append((one_copy, tree_two))
    while len(stack) > 0:
        n1, n2 = stack.pop()
        c1 = n1.get_children(n1)
        c2 = n2.get_children(n2)
        cc = [[0 for _ in range(2)] for _ in range(2)]
        cc[0][0] = c1[0].number_of_leaves()
        cc[0][1] = c1[1].number_of_leaves()
        cc[1][0] = c2[0].number_of_leaves()
        cc[1][1] = c2[1].number_of_leaves()
        if (cc[0][0] - cc[0][1]) * (cc[1][0] - cc[1][1]) < 0:
            n1.children = list()
            n1.addkid(c1[1])
            n1.addkid(c1[0])
        nc1 = n1.get_children(n1)
        for x in range(2):
            if nc1[x].number_of_leaves() > 1 and c2[x].number_of_leaves() > 1:
                stack.append((nc1[x], c2[x]))
    one_copy.fix_complete_tree_list()
    return one_copy

def compare_trees(tree_size, number_of_trees):
    create_random_binary_trees(tree_size, number_of_trees)
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.json'

    if os.path.exists(file_name):
        with open(file_name) as tree_file: 
            tree_list = json.load(tree_file)
        size_start = time.time()
        for i in range(0, min(len(tree_list),number_of_trees)):
            loop_time = time.time()
            j = i + 1
            needed_time = loop_time - size_start
            estimation = needed_time / j * number_of_trees
            print("(" + str(timedelta(seconds=round(needed_time))) + " / " + str(timedelta(seconds=round(estimation)))
                + ") (" + str(j) + "/" + str(number_of_trees) + ") tree size: " + str(tree_size))
            tree_one = create_binary_tree_from_list(tree_list[i]['one'])
            tree_two = create_binary_tree_from_list(tree_list[i]['two'])
            if ('#GRFRestr' not in tree_list[i] and tree_size <= 32):
                I = compute_invalid_edges(tree_one.get_clusters(1), tree_two.get_clusters(1))
                tree_list[i]['#GRFRestr'] = len(I)
            for k in [1]:
                key = 'GRF' + str(k)
                if (key not in tree_list[i] ):
                    start = time.time()
                    print( "k is " + str(k))
                    lp = createLPproblem(tree_one, tree_two, k)
                    time_creation = time.time() - start
                    lp.solve()
                    if LpStatus[lp.status] == "Optimal":
                        end = time.time()
                        varsdict = {}
                        for v in lp.variables():
                            varsdict[v.name] = v.varValue
                        solution = {'clusterOne': json.dumps(tree_one.get_clusters(1)),
                                    'clusterTwo': json.dumps(tree_two.get_clusters(1)),
                                    'vardsDict': json.dumps(varsdict)}
                        tree_list[i]['GRF' + str(k)] = {"cost": value(lp.objective), "time": end - start,
                        "time_creation": time_creation, "solution": solution}
                        
            for k in [0.5]:
                key = "ZSS_" + str(k)
                if (key not in tree_list[i]):
                    start = time.time()
                    print(key)
                    cost = zss.distance(
                            tree_one, tree_two, tree_one.get_children,insert_cost_delta(k), remove_cost_delta(k),
                            update_cost=lambda a, b: strdist(ExtendedNode.get_label(a), ExtendedNode.get_label(b)))
                    end = time.time()
                    tree_list[i][key] = {"cost": cost, "time": end - start}
                #key2 = key + "_a"
                #if (key2 not in tree_list[i]):
                #    start = time.time()
                #    print(key2)
                #   cost = zss.distance(
                 #           tree_one_adapted, tree_two, tree_one.get_children,insert_cost_delta(k), remove_cost_delta(k),
                  #          update_cost=lambda a, b: strdist(ExtendedNode.get_label(a), ExtendedNode.get_label(b)))
                   # end = time.time()
                    #tree_list[i][key2] = {"cost": cost, "time": end - start}

            with open(file_name, 'w') as outfile:
                json.dump(tree_list, outfile)

def create_graph(tree_size, number_of_trees, graph_type="zss_to_grf"):
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.json'
    plot_name = 'plots/' + graph_type + '_trees_size_' + tree_size.__str__() + ".png"
    if os.path.exists(file_name):
        data = [[[] for _ in range(6)] for _ in range(number_of_trees)]
        with open(file_name) as tree_file:
            tree_list = json.load(tree_file)
        if graph_type == 'zss_to_grf':
            for i in range(0, len(tree_list)):
                j = 0
                for k in [1,64]:
                    key = 'GRF' + str(k)
                    if (key in tree_list[i]):
                        data[i][j] = tree_list[i][key]
                    j = j + 1
                if ('ZSS' in tree_list[i]):
                    data[i][3] = tree_list[i]['ZSS']
                if ('ZSS_1' in tree_list[i]):
                    data[i][4] = tree_list[i]['ZSS_1']
                if ('ZSS_1_adapted' in tree_list[i]):
                    data[i][5] = tree_list[i]['ZSS_1_adapted']
            zss1_adapted_to_grf1 = [-1 for _ in range(number_of_trees)]
            zss1_to_grf1 = [-1 for _ in range(number_of_trees)]
            grf64_to_grf1 = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(data)):
                if (len(data) >= 5):
                    if (data[i][4] and data[i][0] and data[i][2]) and data[i][5]:
                        zss1_adapted_to_grf1[i] = float(data[i][5]) / float(data[i][0])
                        zss1_to_grf1[i] = float(data[i][4]) / float(data[i][0])
                        grf64_to_grf1[i] = float(data[i][1]) / float(data[i][0])
            sorted_zss1_to_grf1 = sorted(zss1_to_grf1)
            sorted_grf64_to_grf1 = [x for _,x in sorted(zip(sorted_zss1_to_grf1,grf64_to_grf1))]
            sorted_zss1_adapted_to_grf1 = sorted(zss1_adapted_to_grf1)
            if len(sorted_zss1_to_grf1) > 0 :
                index = len(sorted_zss1_to_grf1) - 1
                maximum = max(np.amax(sorted_zss1_to_grf1), np.amax(sorted_grf64_to_grf1), np.amax(sorted_zss1_adapted_to_grf1))
                plt.ylim(0, max(2.5, 0.2 + maximum))
                plt.plot(sorted_zss1_to_grf1, label="ZSS1 to GRF1")
                plt.plot(sorted_grf64_to_grf1, label="GRF64 to GRF1")
                plt.plot(sorted_zss1_adapted_to_grf1, label="Adapted ZSS1 to GRF1")
                plt.ylabel('proportion of distances relative to GRF 1')
                plt.legend()
                plt.savefig(plot_name)
                plt.figure()
                plt.plot(sorted_zss1_to_grf1, label="ZSS1 to GRF1")
                plt.plot(sorted_zss1_adapted_to_grf1, label="Adapted ZSS1 to GRF1")
                plt.ylabel('proportion of distances relative to GRF 1')
                plt.legend()
                plt.savefig('plots/zss1_sorted_' + tree_size.__str__() + '.png')
                plt.close()
        elif graph_type == 'zss':
            zss_0 = [-1 for _ in range(number_of_trees)]
            zss_0_a = [-1 for _ in range(number_of_trees)]
            zss_0_5 = [-1 for _ in range(number_of_trees)]
            zss_0_5_a = [-1 for _ in range(number_of_trees)]
            zss_1 = [-1 for _ in range(number_of_trees)]
            zss_1_a = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(tree_list)):
                if ('ZSS_0' in tree_list[i]):
                    zss_0[i] = tree_list[i]['ZSS_0'].get('cost') / float(tree_size)
                if ('ZSS_0_a' in tree_list[i]):
                    zss_0_a[i] = tree_list[i]['ZSS_0_a'].get('cost') / float(tree_size)
                if ('ZSS_0.5' in tree_list[i]):
                    zss_0_5[i] = tree_list[i]['ZSS_0.5'].get('cost') / float(tree_size)
                if ('ZSS_0.5_a' in tree_list[i]):
                    zss_0_5_a[i] = tree_list[i]['ZSS_0.5_a'].get('cost') / float(tree_size)
                if ('ZSS_1' in tree_list[i]):
                    zss_1[i] = tree_list[i]['ZSS_1'].get('cost') / float(tree_size)
                if ('ZSS_1_a' in tree_list[i]):
                    zss_1_a[i] = tree_list[i]['ZSS_1_a'].get('cost') / float(tree_size)
            s_zss_0 = sorted(zss_0)
            s_zss_0_a = [x for _,x in sorted(zip(s_zss_0,zss_0_a))]
            s_zss_0_5 = [x for _,x in sorted(zip(s_zss_0,zss_0_5))]
            s_zss_0_5_a = [x for _,x in sorted(zip(s_zss_0,zss_0_5_a))]
            s_zss_1 = [x for _,x in sorted(zip(s_zss_0,zss_1))]
            s_zss_1_a = [x for _,x in sorted(zip(s_zss_0,zss_1_a))]
            s_zss_lin = [(x+y)/2 for x,y in zip(s_zss_0, s_zss_1)]
            s_zss_2_0_5 = [2*x-y for x,y in zip(s_zss_0_5, s_zss_0)]
            maximum = max(np.amax(zss_1), np.amax(zss_1_a))
            plt.ylim(0, maximum + 0.2)
            plt.plot(s_zss_0, label="ZSS 0")
            plt.plot(s_zss_0_a, label="ZSS 0 adapted")
            plt.plot(s_zss_0_5, label="ZSS 0.5")
            plt.plot(s_zss_0_5_a, label="ZSS 0.5 adapted")
            plt.plot(s_zss_1, label="ZSS 1")
            plt.plot(s_zss_1_a, label="ZSS 1 adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig(plot_name)
            plt.close()
        elif graph_type == 'zss_difference':
            zss_0 = [-1 for _ in range(number_of_trees)]
            zss_0_5 = [-1 for _ in range(number_of_trees)]
            zss_1 = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(tree_list)):
                if 'ZSS_0' in tree_list[i] and 'ZSS_0_a' in tree_list[i]:
                    zss_0[i] = tree_list[i]['ZSS_0'].get('cost') - tree_list[i]['ZSS_0_a'].get('cost')
                if 'ZSS_0.5' in tree_list[i] and 'ZSS_0.5_a' in tree_list[i]:
                    zss_0_5[i] = tree_list[i]['ZSS_0.5'].get('cost') - tree_list[i]['ZSS_0.5_a'].get('cost')
                if 'ZSS_1' in tree_list[i] and 'ZSS_1_a' in tree_list[i]:
                    zss_1[i] = tree_list[i]['ZSS_1'].get('cost') - tree_list[i]['ZSS_1_a'].get('cost')
            s_zss_0 = sorted(zss_0)
            s_zss_0_5 = [x for _,x in sorted(zip(s_zss_0,zss_0_5))]
            s_zss_1 = [x for _,x in sorted(zip(s_zss_0,zss_1))]
            maximum = max(np.amax(zss_1), np.amax(zss_0_5), np.amax(zss_0))
            minimum = min(np.amin(zss_1), np.amin(zss_0_5), np.amin(zss_0))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(s_zss_0, label="Differences ZSS 0 and adapted")
            plt.plot(s_zss_0_5, label="Differences ZSS 0.5 and adapted")
            plt.plot(s_zss_1, label="Differences ZSS 1 and adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig(plot_name)
            plt.close()
        elif graph_type == 'zss_differences_adapted':
            zss_0 = [-1 for _ in range(number_of_trees)]
            zss_0_a = [-1 for _ in range(number_of_trees)]
            zss_0_5 = [-1 for _ in range(number_of_trees)]
            zss_0_5_a = [-1 for _ in range(number_of_trees)]
            zss_1 = [-1 for _ in range(number_of_trees)]
            zss_1_a = [-1 for _ in range(number_of_trees)]
            for i in range(0, len(tree_list)):
                if 'ZSS_0' in tree_list[i] and 'ZSS_0_a' in tree_list[i]:
                    zss_0[i] = tree_list[i]['ZSS_0'].get('cost')
                    zss_0_a[i] = tree_list[i]['ZSS_0_a'].get('cost')
                if 'ZSS_0.5' in tree_list[i] and 'ZSS_0.5_a' in tree_list[i]:
                    zss_0_5[i] = tree_list[i]['ZSS_0.5'].get('cost')
                    zss_0_5_a[i] = tree_list[i]['ZSS_0.5_a'].get('cost')
                if 'ZSS_1' in tree_list[i] and 'ZSS_1_a' in tree_list[i]:
                    zss_1[i] = tree_list[i]['ZSS_1'].get('cost')
                    zss_1_a[i] = tree_list[i]['ZSS_1_a'].get('cost')
            s_zss_0 = sorted(zss_0)
            s_zss_0_a = [x for _,x in sorted(zip(s_zss_0,zss_0_a))]
            s_zss_0_5 = sorted(zss_0_5)
            s_zss_0_5_a = [x for _,x in sorted(zip(s_zss_0_5,zss_0_5_a))]
            s_zss_1 = sorted(zss_1)
            s_zss_1_a = [x for _,x in sorted(zip(s_zss_1,zss_1_a))]
            maximum = max(np.amax(zss_0), np.amax(zss_0_a))
            minimum = min(np.amin(zss_0), np.amin(zss_0_a))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(zss_0, label="ZSS 0")
            plt.plot(zss_0_a, label="ZSS 0 adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig('plots/zss0_sorted_' + tree_size.__str__() + '.png')
            plt.close()
            maximum = max(np.amax(zss_0_5), np.amax(zss_0_5_a))
            minimum = min(np.amin(zss_0_5), np.amin(zss_0_5_a))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(zss_0_5, label="ZSS 0.5")
            plt.plot(zss_0_5_a, label="ZSS 0.5 adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig('plots/zss0_5_sorted_' + tree_size.__str__() + '.png')
            plt.close()
            maximum = max(np.amax(zss_1), np.amax(zss_1_a))
            minimum = min(np.amin(zss_1), np.amin(zss_1_a))
            plt.ylim(minimum -0.2, maximum + 0.2)
            plt.plot(zss_1, label="ZSS 1")
            plt.plot(zss_1_a, label="ZSS 1 adapted")
            plt.ylabel('different distance measures')
            plt.legend()
            plt.savefig('plots/zss1_sorted_' + tree_size.__str__() + '.png')
            plt.close()
        elif graph_type == 'low_grf_high_ted':
            zss_0_5 = [-1 for _ in range(number_of_trees)]
            grf_1 = [-1 for _ in range(number_of_trees)]
            for i in range(0, min(len(tree_list), number_of_trees)):
               # key = 'GRF' + str(k)
                if ('GRF1' in tree_list[i]):
                    if isinstance(tree_list[i]['GRF1'], dict) and 'cost' in tree_list[i]['GRF1']:
                        print(i, tree_list[i]['GRF1'].keys(), tree_list[i]['GRF1']) 
                        grf_1[i] = tree_list[i]['GRF1'].get('cost') / float(tree_size)
                    elif isinstance(tree_list[i]['GRF1'],(int,float)):
                        grf_1[i] = tree_list[i]['GRF1']
                if ('ZSS_0.5' in tree_list[i]):
                    zss_0_5[i] = tree_list[i]['ZSS_0.5'].get('cost') / float(tree_size)
            s_grf_1 = sorted(grf_1)
            s_zss_0_5 = [x for _,x in sorted(zip(grf_1,zss_0_5))]
            low_grf_1 = [s_grf_1[i] for i in range(0,21)];
            low_zss_0_5 = [s_zss_0_5[i] for i in range(0,21)];
            high_grf_1 = [s_grf_1[i] for i in range(119,140)];
            high_zss_0_5 = [s_zss_0_5[i] for i in range(119,140)];
            if len(low_grf_1) > 0 and len(low_zss_0_5) > 20:
                maximum = max(np.amax(low_grf_1), np.amax(low_zss_0_5))
                plot_name = 'plots/low_grf_corr_ated.png'
                plt.ylim(0, max(2.5, 0.2 + maximum))
                plt.plot(low_grf_1, label="lowest gRFs")
                plt.plot(low_zss_0_5, label="corresponding ATED")
                plt.ylabel('distance values')
                plt.xlabel('example count')
                plt.legend()
                plt.savefig(plot_name)
                plt.figure()
                plt.close()
            if len(high_grf_1) > 0 and len(high_zss_0_5) > 20:
                maximum = max(np.amax(high_grf_1), np.amax(high_zss_0_5))
                plot_name = 'plots/high_grf_corr_ated.png'
                plt.ylim(0, max(2.5, 0.2 + maximum))
                plt.plot(high_grf_1, label="highest gRFs")
                plt.plot(high_zss_0_5, label="corresponding ATED")
                plt.ylabel('distance values')
                plt.xlabel('example count')
                plt.legend()
                plt.savefig(plot_name)
                plt.figure()
                plt.close()

def create_time_graph():
    k_array = [4,5,6,7,8,9,10,11,12,16,20,24,32,40,48,64,128,192,256]
    ar_zss_0 = []
    ar_zss_0_a = []
    ar_zss_0_5 = []
    ar_zss_0_5_a = []
    ar_zss_1 = []
    ar_zss_1_a = []
    ar_grf1 = []
    ar_grf64 = []
    for k in k_array:
        zss_0 = zss_0_a = zss_0_5 = zss_0_5_a = zss_1 = zss_1_a = grf1 = grf64 = {'time': 0, 'count': 0}
        file_name = 'examples/example_trees_size_' + k.__str__() + '.json'
        if os.path.exists(file_name):
            with open(file_name) as tree_file:
                tree_list = json.load(tree_file)
            for tree in tree_list:
                if 'GRF1' in tree and tree['GRF1'].get('time'):
                    grf1 = {'time': grf1.get('time') + tree['GRF1'].get('time'), 'count': grf1.get('count') + 1}
                if 'GRF64' in tree and tree['GRF64'].get('time'):
                    grf64 = {'time': grf64.get('time') + tree['GRF64'].get('time')
                        , 'count': grf64.get('count') + 1}
                if 'ZSS_0' in tree and tree['ZSS_0'].get('time'):
                    zss_0 = {'time': zss_0.get('time') + tree['ZSS_0'].get('time')
                        , 'count': zss_0.get('count') + 1}
                if 'ZSS_0_a' in tree and tree['ZSS_0_a'].get('time'):
                    zss_0_a = {'time': zss_0_a.get('time') + tree['ZSS_0_a'].get('time')
                        , 'count': zss_0_a.get('count') + 1}
                if 'ZSS_0.5' in tree and tree['ZSS_0.5'].get('time'):
                    zss_0_5 = {'time': zss_0.get('time') + tree['ZSS_0.5'].get('time')
                        , 'count': zss_0_5.get('count') + 1}
                if 'ZSS_0.5_a' in tree and tree['ZSS_0.5_a'].get('time'):
                    zss_0_5_a = {'time': zss_0_5_a.get('time') + tree['ZSS_0.5_a'].get('time')
                        , 'count': zss_0_5_a.get('count') + 1}
                if 'ZSS_1' in tree and tree['ZSS_1'].get('time'):
                    zss_1 = {'time': zss_1.get('time') + tree['ZSS_1'].get('time')
                        , 'count': zss_1.get('count') + 1}
                if 'ZSS_1_a' in tree and tree['ZSS_1_a'].get('time'):
                    zss_1_a =  {'time': zss_1_a.get('time') + tree['ZSS_1_a'].get('time')
                        , 'count': zss_1_a.get('count') + 1}

            if zss_0.get('count'):
                 ar_zss_0.append(zss_0.get('time') / zss_0.get('count'))
            if zss_0_a.get('count'):
                 ar_zss_0_a.append(zss_0_a.get('time') / zss_0_a.get('count'))
            if zss_0_5.get('count'):
                 ar_zss_0_5.append(zss_0.get('time') / zss_0_5.get('count'))
            if zss_0_5_a.get('count'):
                 ar_zss_0_5_a.append(zss_0_5_a.get('time') / zss_0_5_a.get('count'))
            if zss_1.get('count'):
                ar_zss_1.append(zss_1.get('time') / zss_1.get('count'))
            if zss_1_a.get('count'):
                ar_zss_1_a.append(zss_1_a.get('time') / zss_1_a.get('count'))
            if grf1.get('count') > 5:
                ar_grf1.append(grf1.get('time') / grf1.get('count'))
            if grf64.get('count') > 5:
                ar_grf64.append(grf64.get('time') / grf64.get('count'))
    maximum = max(np.amax(ar_grf64), np.amax(ar_grf1), np.amax(ar_zss_1_a), np.amax(ar_zss_1))

    # time plot all
    plt.figure()
    plt.ylim(0, 1000)
    plt.plot(k_array, ar_zss_0, label="ZSS 0")
    plt.plot(k_array, ar_zss_0_a, label="ZSS 0 adapted")
    plt.plot(k_array, ar_zss_0_5, label="ZSS 0.5")
    plt.plot(k_array, ar_zss_0_5_a, label="ZSS 0.5 adapted")
    plt.plot(k_array, ar_zss_1, label="ZSS 1")
    plt.plot(k_array, ar_zss_1_a, label="ZSS 1 adapted")
    plt.plot(k_array[0:len(ar_grf1)], ar_grf1, label="gRF 1")
    plt.plot(k_array[0:len(ar_grf64)], ar_grf64, label="gRF 64")
    plt.ylabel('time taken for the different approaches')
    plt.legend()
    plt.savefig('plots/time_plot_all.png')
    plt.figure()
    plt.close()

    # time plot zss
    plt.figure()
    plt.ylim(0, 1000)
    plt.plot(k_array, ar_zss_0, label="ZSS 0")
    plt.plot(k_array, ar_zss_0_a, label="ZSS 0 adapted")
    plt.plot(k_array, ar_zss_0_5, label="ZSS 0.5")
    plt.plot(k_array, ar_zss_0_5_a, label="ZSS 0.5 adapted")
    plt.plot(k_array, ar_zss_1, label="ZSS 1")
    plt.plot(k_array, ar_zss_1_a, label="ZSS 1 adapted")
    plt.ylabel('time taken for the different approaches')
    plt.legend()
    plt.savefig('plots/time_plot_zss.png')
    plt.close()


    # time plot grf / zss
    plt.figure()
    plt.ylim(0, 1000)
    plt.plot(k_array, ar_zss_1, label="Tree Edit Distance")
    plt.plot(k_array[0:len(ar_grf1)], ar_grf1, label="generalized Robinson Foulds")
    plt.ylabel('average time taken for the different approaches (in s)')
    plt.xlabel('number of leaves on each example tree')
    plt.legend()
    plt.savefig('plots/time_plot_all.png')
    plt.figure()
    plt.close()


def compute_results():
    k_array = [4,5,6,7,8,9,10,11,12,16,20,24,32,40,48,64,128,192,256]
    ar_zss_0 = {"time": [], "cost": [], "max": [], "min": []}
    ar_zss_0_a = {"time": [], "cost": [], "max": [], "min": []}
    ar_zss_0_5 = {"time": [], "cost": [], "max": [], "min": []}
    ar_zss_0_5_a = {"time": [], "cost": [], "max": [], "min": []}
    ar_zss_1 = {"time": [], "cost": [], "max": [], "min": []}
    ar_zss_1_a = {"time": [], "cost": [], "max": [], "min": []}
    ar_grf1 = {"time": [], "cost": [], "max": [], "min": []}
    ar_grf64 = {"time": [], "cost": [], "max": [], "min": []}
    for k in k_array:
        zss_0 = zss_0_a = zss_0_5 = zss_0_5_a = zss_1 = zss_1_a = grf1 = grf64 = {'time': 0, 'cost': 0, 'count': 0,
        'max': 0, 'min': 9999999}
        file_name = 'examples/example_trees_size_' + k.__str__() + '.json'
        if os.path.exists(file_name):
            with open(file_name) as tree_file:
                tree_list = json.load(tree_file)
            for tree in tree_list:
                if 'GRF1' in tree and tree['GRF1'].get('time') and tree['GRF1'].get('cost') :
                    grf1 = {
                        'time': grf1.get('time') + tree['GRF1'].get('time'),
                        'cost': grf1.get('cost') + tree['GRF1'].get('cost') / k,
                        'count': grf1.get('count') + 1,
                        'max': max(grf1.get('max'), tree['GRF1'].get('cost')),
                        'min': min(grf1.get('min'), tree['GRF1'].get('cost'))
                        }

                if 'GRF64' in tree and tree['GRF64'].get('time') and tree['GRF64'].get('cost'):
                    grf64 = {
                        'time': grf64.get('time') + tree['GRF64'].get('time'),
                        'cost': grf64.get('cost') + tree['GRF64'].get('cost') / k,
                        'count': grf64.get('count') + 1,
                        'max': max(grf64.get('max'), tree['GRF64'].get('cost')),
                        'min': min(grf64.get('min'), tree['GRF64'].get('cost'))
                        }

                if 'ZSS_0' in tree and tree['ZSS_0'].get('time') and tree['ZSS_0'].get('cost'):
                    zss_0 = {
                        'time': zss_0.get('time') + tree['ZSS_0'].get('time'),
                        'cost': zss_0.get('cost') + tree['ZSS_0'].get('cost') / k,
                        'count': zss_0.get('count') + 1,
                        'max': max(zss_0.get('max'), tree['ZSS_0'].get('cost')),
                        'min': min(zss_0.get('min'), tree['ZSS_0'].get('cost'))
                        }

                if 'ZSS_0_a' in tree and tree['ZSS_0_a'].get('time') and tree['ZSS_0_a'].get('cost'):
                    zss_0_a = {
                        'time': zss_0_a.get('time') + tree['ZSS_0_a'].get('time'),
                        'cost': zss_0_a.get('cost') + tree['ZSS_0_a'].get('cost') / k,
                        'count': zss_0_a.get('count') + 1,
                        'max': max(zss_0_a.get('max'), tree['ZSS_0_a'].get('cost')),
                        'min': min(zss_0_a.get('min'), tree['ZSS_0_a'].get('cost'))
                        }

                if 'ZSS_0.5' in tree and tree['ZSS_0.5'].get('time') and tree['ZSS_0.5'].get('cost'):
                    zss_0_5 = {
                        'time': zss_0_5.get('time') + tree['ZSS_0.5'].get('time'),
                        'cost': zss_0_5.get('cost') + tree['ZSS_0.5'].get('cost') / k,
                        'count': zss_0_5.get('count') + 1,
                        'max': max(zss_0_5.get('max'), tree['ZSS_0.5'].get('cost')),
                        'min': min(zss_0_5.get('min'), tree['ZSS_0.5'].get('cost'))
                        }

                if 'ZSS_0.5_a' in tree and tree['ZSS_0.5_a'].get('time')  and tree['ZSS_0.5_a'].get('cost'):
                    zss_0_5_a = {
                        'time': zss_0_5_a.get('time') + tree['ZSS_0.5_a'].get('time'),
                        'cost': zss_0_5_a.get('cost') + tree['ZSS_0.5_a'].get('cost') / k,
                        'count': zss_0_5_a.get('count') + 1,
                        'max': max(zss_0_5_a.get('max'), tree['ZSS_0.5_a'].get('cost')),
                        'min': min(zss_0_5_a.get('min'), tree['ZSS_0.5_a'].get('cost'))
                        }

                if 'ZSS_1' in tree and tree['ZSS_1'].get('time') and tree['ZSS_1'].get('cost'):
                    zss_1 = {
                        'time': zss_1.get('time') + tree['ZSS_1'].get('time'),
                        'cost': zss_1.get('cost') + tree['ZSS_1'].get('cost') / k,
                        'count': zss_1.get('count') + 1,
                        'max': max(zss_1.get('max'), tree['ZSS_1'].get('cost')),
                        'min': min(zss_1.get('min'), tree['ZSS_1'].get('cost'))
                        }

                if 'ZSS_1_a' in tree and tree['ZSS_1_a'].get('time') and tree['ZSS_1_a'].get('cost'):
                    zss_1_a =  {
                        'time': zss_1_a.get('time') + tree['ZSS_1_a'].get('time'),
                        'cost': zss_1_a.get('cost') + tree['ZSS_1_a'].get('cost') / k,
                        'count': zss_1_a.get('count') + 1,
                        'max': max(zss_1_a.get('max'), tree['ZSS_1_a'].get('cost')),
                        'min': min(zss_1_a.get('min'), tree['ZSS_1_a'].get('cost'))
                        }
            if zss_0.get('count'):
                ar_zss_0["time"].append(zss_0.get('time') / zss_0.get('count'))
                ar_zss_0["cost"].append(zss_0.get('cost') / zss_0.get('count'))
                ar_zss_0["max"].append(zss_0.get('max'))
                ar_zss_0["min"].append(zss_0.get('min'))
            if zss_0_a.get('count'):
                ar_zss_0_a["time"].append(zss_0_a.get('time') / zss_0_a.get('count'))
                ar_zss_0_a["cost"].append(zss_0_a.get('cost') / zss_0_a.get('count'))
                ar_zss_0_a["max"].append(zss_0_a.get('max'))
                ar_zss_0_a["min"].append(zss_0_a.get('min'))
            if zss_0_5.get('count'):
                ar_zss_0_5["time"].append(zss_0_5.get('time') / zss_0_5.get('count'))
                ar_zss_0_5["cost"].append(zss_0_5.get('cost') / zss_0_5.get('count'))
                ar_zss_0_5["max"].append(zss_0_5.get('max'))
                ar_zss_0_5["min"].append(zss_0_5.get('min'))
            if zss_0_5_a.get('count'):
                ar_zss_0_5_a["time"].append(zss_0_5_a.get('time') / zss_0_5_a.get('count'))
                ar_zss_0_5_a["cost"].append(zss_0_5_a.get('cost') / zss_0_5_a.get('count'))
                ar_zss_0_5_a["max"].append(zss_0_5_a.get('max'))
                ar_zss_0_5_a["min"].append(zss_0_5_a.get('min'))
            if zss_1.get('count'):
                ar_zss_1["time"].append(zss_1.get('time') / zss_1.get('count'))
                ar_zss_1["cost"].append(zss_1.get('cost') / zss_1.get('count'))
                ar_zss_1["max"].append(zss_1.get('max'))
                ar_zss_1["min"].append(zss_1.get('min'))
            if zss_1_a.get('count'):
                ar_zss_1_a["time"].append(zss_1_a.get('time') / zss_1_a.get('count'))
                ar_zss_1_a["cost"].append(zss_1_a.get('cost') / zss_1_a.get('count'))
                ar_zss_1_a["max"].append(zss_1_a.get('max'))
                ar_zss_1_a["min"].append(zss_1_a.get('min'))
            if grf1.get('count') > 5:
                ar_grf1["time"].append(grf1.get('time') / grf1.get('count'))
                ar_grf1["cost"].append(grf1.get('cost') / grf1.get('count'))
                ar_grf1["max"].append(grf1.get('max'))
                ar_grf1["min"].append(grf1.get('min'))
            if grf64.get('count') > 5:
                ar_grf64["time"].append(grf64.get('time') / grf64.get('count'))
                ar_grf64["cost"].append(grf64.get('cost') / grf64.get('count'))
                ar_grf64["max"].append(grf64.get('max'))
                ar_grf64["min"].append(grf64.get('min'))

    differences = {
        'ZSS_0': [],
        'ZSS_0_5': [],
        'ZSS_1': [],
        }
    for i in range(0, len(k_array)):
        differences['ZSS_0'].append(ar_zss_0['cost'][i] - ar_zss_0_a['cost'][i])
        differences['ZSS_0_5'].append(ar_zss_0_5['cost'][i] - ar_zss_0_5_a['cost'][i])
        differences['ZSS_1'].append(ar_zss_1['cost'][i] - ar_zss_1_a['cost'][i])


    result_data = {
        'GRF1': ar_grf1,
        'GRF64': ar_grf64,
        'ZSS_0': ar_zss_0,
        'ZSS_0_a': ar_zss_0_a,
        'ZSS_0_5': ar_zss_0_5,
        'ZSS_0_5_a': ar_zss_0_5_a,
        'ZSS_1': ar_zss_1,
        'ZSS_1_a': ar_zss_1_a,
        'Differences adapted': differences
        }
    with open('results/result_data.json', 'w') as outfile:
        json.dump(result_data, outfile)

if __name__ == "__main__":
    for tree_size in [8]:
        number_of_trees = 3
        compare_trees(tree_size, number_of_trees)
        create_graph(tree_size, number_of_trees, "low_grf_high_ted")
    #compute_results()
    #create_time_graph()

