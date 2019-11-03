from extended_node import ExtendedNode
from datetime import datetime
import gurobipy
import catalan_numbers
import random
import json
import os

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
        new_tree_list = random_full_binary_tree(tree_size).get_list()
        new_tree_list.label_leaves_randomly()
        append = 1 

        for tree in tree_list:
            if new_tree_list.__str__() == tree.__str__():
                append = 0

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
        return ExtendedNode(0, [create_binary_tree_from_list(list[0]), create_binary_tree_from_list(list[1])])

def distance_between_clusters(cluster_one, cluster_two, k):
    cap = [i for i in cluster_one if i in cluster_two]
    in_second_but_not_in_first = [i for i in cluster_two if i not in cluster_one ]
    cup = cluster_one + in_second_but_not_in_first
    
    return 1 - (len(cap) / len(cup))**k

def compute_cost_function(cluster_one, cluster_two, k):
    return {(i,j): distance_between_clusters(cluster_one[i], cluster_two[j], k) for i in range(0, len(cluster_one)) for j in range(0, len(cluster_two))}

if __name__ == "__main__":
    tree_size = int(input("Number of leaves:"))
    #number_of_trees = int(input("Number of trees:"))
    #create_random_binary_trees(tree_size, number_of_trees)
    tree_one = random_full_binary_tree(tree_size)
    tree_two = random_full_binary_tree(tree_size)
    tree_one.label_leaves_randomly()
    tree_two.label_leaves_randomly() 
    clusters_one = tree_one.get_clusters(1)
    clusters_two = tree_two.get_clusters(1)
    c = compute_cost_function(clusters_one, clusters_two, 4)
    print(clusters_one, clusters_two)
    print(c)

