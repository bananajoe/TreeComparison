from __future__ import absolute_import
from extended_node import ExtendedNode
from datetime import datetime
from pulp import *
import catalan_numbers
import random
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

def insert_cost_advanced(node):
    if (ExtendedNode.get_label(node) != 0):
        return strdist('', ExtendedNode.get_label(node))
    else:
        return 0

def remove_cost_advanced(node):
    if (ExtendedNode.get_label(node) != 0):
        return strdist(ExtendedNode.get_label(node), '')
    else:
        return 0

def random_full_binary_tree(n):
    if n == 1:
        return ExtendedNode(n)
    else:
        catalan = catalan_numbers.load_catalan_numbers_until(n)
        lower = 0
        r = random.random()
        for i in range(1,n):
            p = (catalan[i-1] * catalan[n-i-1]) / catalan[n-1]
            upper = lower + p
            if lower <= r and r < upper:
                break
            lower = upper

        return ExtendedNode(n, [random_full_binary_tree(i), random_full_binary_tree(n-i)])

def random_full_binary_tree_stack(n):
    stack = list()
    root = ExtendedNode(n)
    stack.append(root)
    while len(stack) > 0:
        node = stack.pop()
        n = node.get_label(node)
        if n > 1:
            catalan = catalan_numbers.load_catalan_numbers_until(n)
            lower = 0
            r = random.random()
            for i in range(1,n):
                p = (catalan[i-1] * catalan[n-i-1]) / catalan[n-1]
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
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.txt'

    if os.path.exists(file_name):
        with open(file_name) as tree_file: 
            tree_list = json.load(tree_file)
    else:
        tree_list = []

    current_list_length = len(tree_list)
    safety_net = 0
    while current_list_length < number_of_trees and safety_net < 10 * number_of_trees:
        new_tree_one_list = random_full_binary_tree(tree_size)
        new_tree_one_list.label_leaves_randomly()
        new_tree_one_list = new_tree_one_list.get_list()
        new_tree_two_list = random_full_binary_tree(tree_size)
        new_tree_two_list.label_leaves_randomly()
        new_tree_two_list = new_tree_two_list.get_list()
        
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

def create_binary_tree_from_list(list, label):
    if len(list) == 1:
        return ExtendedNode(list[0])
    elif len(list) == 2:
        label = label + 1
        return ExtendedNode(label, [create_binary_tree_from_list(list[0], label), create_binary_tree_from_list(list[1],label-10)])

def distance_between_clusters(cluster_one, cluster_two, k):
    cap = [i for i in cluster_one if i in cluster_two]
    in_second_but_not_in_first = [i for i in cluster_two if i not in cluster_one ]
    cup = cluster_one + in_second_but_not_in_first
    return 1 - (len(cap) / len(cup))**k

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

def compare_trees(tree_size, number_of_trees):
    create_random_binary_trees(tree_size, number_of_trees)
    file_name = 'examples/example_trees_size_' + tree_size.__str__() + '.txt'

    if os.path.exists(file_name):
        with open(file_name) as tree_file: 
            tree_list = json.load(tree_file)
        for i in range(0, len(tree_list)):
            tree_one = create_binary_tree_from_list(tree_list[i]['one'])
            tree_two = create_binary_tree_from_list(tree_list[i]['two'])
            for k in [1,2,4,16,128]:
                key = 'GRF' + str(k)
                if (key not in tree_list[i]):
                    lp = createLPproblem(tree_one, tree_two, k)
                    lp.solve()
                    if LpStatus[lp.status] == "Optimal":
                        tree_list[i]['GRF' + str(k)] = value(lp.objective)
            if ('ZSS' not in tree_list[i]):
                tree_list[i]['ZSS'] = zss.simple_distance(tree_one, tree_two)
            if ('ZSS_1' not in tree_list[i]):
                tree_list[i]['ZSS_1'] = zss.distance(
        tree_one, tree_two, tree_one.get_children,insert_cost_advanced, remove_cost_advanced,
        update_cost=lambda a, b: strdist(ExtendedNode.get_label(a), ExtendedNode.get_label(b)))
        with open(file_name, 'w') as outfile:
            json.dump(tree_list, outfile)  



class AnnTree(object):

    def __init__(self, root, get_children):
        self.get_children = get_children

        self.root = root
        self.nodes = list()  # a post-order enumeration of the nodes in the tree
        self.ids = list()    # a matching list of ids
        self.lmds = list()   # left most descendents
        self.keyroots = None
            # k and k' are nodes specified in the post-order enumeration.
            # keyroots = {k | there exists no k'>k such that lmd(k) == lmd(k')}
            # see paper for more on keyroots

        stack = list()
        pstack = list()
        stack.append((root, collections.deque()))
        j = 0
        while len(stack) > 0:
            n, anc = stack.pop()
            nid = j
            for c in self.get_children(n):
                a = collections.deque(anc)
                a.appendleft(nid)
                stack.append((c, a))
                print(a, n.get_label(n))
            print(n.get_label(n), nid)
            pstack.append(((n, nid), anc))
            j += 1 
        lmds = dict()
        keyroots = dict()
        i = 0
        while len(pstack) > 0:
            (n, nid), anc = pstack.pop()
            self.nodes.append(n)
            self.ids.append(nid)
            if not self.get_children(n):
                lmd = i
                for a in anc:
                    if a not in lmds: lmds[a] = i
                    else: break
            else:
                try: lmd = lmds[nid]
                except:
                    import pdb
                    pdb.set_trace()
            self.lmds.append(lmd)
            keyroots[lmd] = i
            i += 1
        self.keyroots = sorted(keyroots.values())


if __name__ == "__main__":
    file_name = 'examples/example.txt'
    if os.path.exists(file_name):
        with open(file_name) as tree_file: 
            tree_list = json.load(tree_file)
    else:
        tree_list = []

    for i in range(0, len(tree_list)):
        tree_one = create_binary_tree_from_list(tree_list[i]['one'], -5)
        ann_tree = AnnTree(tree_one, ExtendedNode.get_children)   
           